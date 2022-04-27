"""Test cli commands"""
from unittest.mock import Mock, patch

from click.testing import CliRunner

from inky_pi.cli import cli


@patch("inky_pi.main.InkyDraw")
def test_cli_inky(_: Mock) -> None:
    """Tests inky_pi inky command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["inky", "--dry-run"])
    assert result.exit_code == 0


@patch("inky_pi.main.InkyDraw")
def test_cli_weather(_: Mock) -> None:
    """Tests inky_pi weather command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["weather", "--dry-run"])
    assert result.exit_code == 0


@patch("inky_pi.main.InkyDraw")
def test_cli_goodnight(_: Mock) -> None:
    """Tests inky_pi goodnight command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["night", "--dry-run"])
    assert result.exit_code == 0
