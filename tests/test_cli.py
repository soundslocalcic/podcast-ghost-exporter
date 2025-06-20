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


@mock_http("cli", "test_transistor")
def test_transistor():
    """
    Run CLI command with a valid feed URL.

    Arrange/Act: Run the CLI subcommand with a URL parameter.
    Assert: The output is a valid Ghost JSON document.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli,
        ["https://feeds.transistor.fm/undo"]
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
        db["data"]["posts"][0]["id"] == "1e42894556c3ab3218d475253b1e9845"
    ), "Incorrect item ID."


@mock_http("cli", "test_buzzsprout")
def test_buzzsprout():
    """
    Run CLI command with a valid feed URL.

    Arrange/Act: Run the CLI subcommand with a URL parameter.
    Assert: The output is a valid Ghost JSON document.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli.cli,
        ["https://feeds.buzzsprout.com/156239.rss"]
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
        db["data"]["posts"][0]["id"] == "abe64cf9e68177cedc1add251dd46b6f"
    ), "Incorrect item ID."
