import pytest
from click.testing import CliRunner
from surge import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    pass


def test_cli_with_option(runner):
    pass


def test_cli_with_arg(runner):
    pass
