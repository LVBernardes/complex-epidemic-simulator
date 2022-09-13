"""Nox sessions."""
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import nox
from nox.sessions import Session

package = "complex_epidemic_simulator"
locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "safety", "tests"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """
    Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Parameters
    ----------
    session: Session
        The Session object.
    *args: str
        Command-line arguments for pip.
    **kwargs: Any
        Additional keyword arguments for Session.install.
    """
    with TemporaryDirectory() as tmpdir:
        temp_req_file_name = f"requirements_{str(uuid.uuid4())[:6]}.txt"
        temp_req_file_path = Path(tmpdir).joinpath(temp_req_file_name)
        session.run(
            "poetry",
            "export",
            "--only=dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={temp_req_file_path}",
            external=True,
        )
        session.install(f"--requirement={temp_req_file_path}", *args, **kwargs)


@nox.session(python=["3.9", "3.10", "pypy3.9"])
def tests(session: Session) -> None:
    """Execute unit and integration tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python="3.9")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.9")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.9")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.9")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.9", "3.10"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with TemporaryDirectory() as tmpdir:
        temp_req_file_name = f"requirements_{str(uuid.uuid4())[:6]}.txt"
        temp_req_file_path = Path(tmpdir).joinpath(temp_req_file_name)
        session.run(
            "poetry",
            "export",
            "--only=dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={temp_req_file_path}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={temp_req_file_path}", "--full-report")


@nox.session(python="3.9")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python=["3.9", "3.10"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.9")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
