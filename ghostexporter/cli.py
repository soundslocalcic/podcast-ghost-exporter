"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: ghostexporter.cli
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from . import hooks, playback
from .models import Feed
import click
import logging
import sys


LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG
}  #: a mapping of `verbose` option counts to logging levels


DEFAULT_VERSION = "5"


@click.command()
@click.argument("url")
@click.option("--version", default=DEFAULT_VERSION, help="Document version number.")  # noqa
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
def cli(url: str, version: str = DEFAULT_VERSION, verbose: int = 0):
    """Convert a podcast RSS feed into a Ghost JSON document."""
    # Use the verbosity count to determine the logging level
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )

        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )

    hooks.emit("ready")
    feed = Feed(url)
    doc = feed.items.to(version)
    doc.write(sys.stdout)
