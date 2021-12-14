#!/usr/bin/python
# -*- coding: ascii -*-
"""
Pure built-in based virtual environment activator and executor.

- Activates, if possible, the project's virtual environment.
- Execute the desired command.

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
def search() -> tp.Optional[pl.Path]:
    """
    Search and returns the project environment's path.

    :return: Path to project's VENV, if exists.
    :rtype: tp.Optional[pl.Path]
    """
    find = list(ROOT.rglob(pattern="python.exe"))
    return find.pop().parent.parent if find else None


def activate(venv: pl.Path) -> None:
    """
    Activates the given virtual environment on the current run.

    :param pl.Path venv:        Path to virtualenv folder.
    """
    # Get environment paths
    bins = venv / "Scripts"
    libs = venv / "Libs/site-packages"

    # Register environment
    os.environ["VIRTUAL_ENV"] = f"{venv}"

    # Add binaries to path
    os.environ["PATH"] = f"{bins}{os.pathsep}{os.environ['PATH']}"

    # Add libraries to host python
    idx = len(sys.path)
    site.addsitedir(sitedir=libs)
    sys.path = sys.path[idx:] + sys.path[0:idx]

    # Update system prefix
    sys.old_prefix = sys.prefix
    sys.prefix = f"{venv}"

    # Verify
    active = pl.Path(sys.prefix)
    if venv != active:
        raise EnvironmentError(f"Active environment doesn't match target: {venv} != {active}.")


def execute() -> None:
    """
    Tries to activate the project virtual environment and execute the provided command.
    """
    activate(venv=search())
    cmd = f"python {' '.join(sys.argv[1:])}"
    print(
        f"Executing..."
        f"\nEnv: {sys.prefix}"
        f"\nCwd: {os.getcwd()}"
        f"\nCmd: {cmd}\n"
        )
    sys.stdout.flush()
    sp.call(cmd, cwd=os.getcwd(), shell=True)


# -->> Execute <<----------------------
if __name__ == '__main__':
    execute()
