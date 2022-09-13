"""Simulator console module."""

import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Execute the hello world command."""
    click.echo("Hello, world!")
