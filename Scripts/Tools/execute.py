#!/usr/bin/python
# -*- coding: ascii -*-
"""
Execution tool.

- Activates, if possible, the project's virtual environment.
- Executed the desired command.

:date:      2021
:author:    cwichel
:contact:   cwichel@gmail.com
:license:   The MIT License (MIT)
"""

import os
import pathlib as pl
import site
import subprocess as sp
import sys
import typing as tp


# -->> Tunables <<---------------------


# -->> Definitions <<------------------
#: Project ROOT path
ROOT = pl.Path(os.path.dirname(__file__)).parent.parent


# -->> API <<--------------------------
def _venv_search() -> tp.Optional[pl.Path]:
    """
    Search and returns the project environment's path.

    :return: Path to project's VENV, if exists.
    :rtype: tp.Optional[pl.Path]
    """
    find = list(ROOT.rglob(pattern="python.exe"))
    return find.pop().parent.parent if find else None


def _venv_activate_script(path: pl.Path) -> None:
    """
    Activates the virtual environment using the provided script.

    :param pl.Path path: Path to the activation script.

    """
    # Executes the script in the current process
    with path.open(mode="r", encoding="utf-8") as file:
        code = compile(file.read(), path, "exec")
        exec(code, dict(__file__=path))


def _venv_activate_manual(path: pl.Path) -> None:
    """
    Activates the environment manually.

    :param pl.Path path: Path to the virtual environment folder.

    """
    # Get environment paths
    bins = path / "Scripts"
    libs = path / "Libs/site-packages"

    # Register environment
    os.environ["VIRTUAL_ENV"] = f"{path}"

    # Add binaries to path
    os.environ["PATH"] = f"{bins}{os.pathsep}{os.environ['PATH']}"

    # Add libraries to host python
    idx = len(sys.path)
    site.addsitedir(sitedir=libs)
    sys.path = sys.path[idx:] + sys.path[0:idx]

    # Update system prefix
    sys.real_prefix = sys.prefix
    sys.prefix = f"{path}"


def venv_activate() -> None:
    """
    Activates the environment, if available.
    """
    # Get environment path
    venv = _venv_search()
    if venv is None:
        return

    # Activate
    script = venv / "Scripts/activate_this.py"
    if script.exists() and script.is_file():
        _venv_activate_script(path=script)
    else:
        _venv_activate_manual(path=venv)

    # Verify
    active = pl.Path(sys.prefix)
    if venv != active:
        raise EnvironmentError(f"Active environment doesn't match target: {venv} != {active}.")


def execute() -> None:
    """
    Tries to activate the project virtual environment and execute the provided command.
    """
    cmd = " ".join(sys.argv[1:])
    venv_activate()
    print(
        f"Executing..."
        f"\nEnv: {sys.prefix}"
        f"\nCwd: {os.getcwd()}"
        f"\nCmd: {cmd}"
        )
    sp.call(f"{cmd}", cwd=os.getcwd(), shell=True)


# -->> Execute <<----------------------
if __name__ == '__main__':
    execute()
