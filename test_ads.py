import pytest
from click.testing import CliRunner

from ads_cli import cli


def test_hello():
    runner = CliRunner()
    result = runner.invoke(cli, ["download", "blah"])
    assert result is None

