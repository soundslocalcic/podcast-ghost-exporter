"""
Unit tests.

.. currentmodule:: test_cli
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>

This is the test module for the project's command-line interface (CLI)
module.
"""

from click.testing import CliRunner, Result
from .utils import mock_http
import ghostexporter.cli as cli
import json


def test_no_url():
    """
    Run CLI command with no URL.

    Arrange/Act: Run the CLI subcommand with no parameters.
    Assert: The output produces an argument error.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli)
    assert (
        "Error: Missing argument 'URL'." in result.output.strip()
    ), "URL argument must be enforced."


@mock_http("cli", "test_valid_url")
def test_valid_url():
    """
    Run CLI command with a valid feed URL.

    Arrange/Act: Run the CLI subcommand with a URL parameter.
    Assert: The output is a valid Ghost JSON document.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli,
        ["https://feeds.transistor.fm/listenvy"]
    )

    try:
        doc = json.loads(result.output.strip())
    except Exception:
        raise result.exception

    db = doc["db"][0]

    assert (
        db["meta"]["version"] == "5.125.0-0-g09f7924d"
    ), "Incorrect verison number."

    assert (
        db["data"]["posts"][0]["id"] == "34b4141d2ec76c1b0e26557ceedf5ceb"
    ), "Incorrect item ID."
