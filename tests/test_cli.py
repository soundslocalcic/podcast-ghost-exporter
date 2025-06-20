"""
Unit tests.

.. currentmodule:: test_cli
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>

This is the test module for the project's command-line interface (CLI)
module.
"""

from click.testing import CliRunner, Result
from unittest import mock
import ghostexporter.cli as cli
import json
import os


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


class MockResponse(object):
    """Mock requests.Response object."""

    def __init__(self, url):
        """Initialise the mock response."""
        pass

    def raise_for_status(self):
        """Raise an error corresponding to the HTTP response code."""
        pass

    @property
    def content(self):
        """Return a binary string of data."""
        filename = os.path.join(
            os.path.join(os.path.dirname(__file__)),
            "fixtures",
            "test_feed.xml"
        )

        with open(filename, "rb") as f:
            return f.read()


@mock.patch("requests.get", MockResponse)
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

    doc = json.loads(result.output.strip())
    db = doc["db"][0]

    assert (
        db["meta"]["version"] == "5.125.0-0-g09f7924d"
    ), "Incorrect verison number."

    assert (
        db["data"]["posts"][0]["id"] == "61aad99f07d4984d490d5c85bc55dd0c"
    ), "Incorrect item ID."
