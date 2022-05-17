"""Test cli commands"""

from click.testing import CliRunner

from inky_pi.cli import (
    DESKTOP_ECHO,
    NIGHT_ECHO,
    TERMINAL_ECHO,
    TRAIN_ECHO,
    WEATHER_ECHO,
    cli,
)


def test_cli_main() -> None:
    """Tests inky_pi main command"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]" in result.output


def test_cli_train() -> None:
    """Tests inky_pi inky command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["train", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == f"{TRAIN_ECHO}\n"


def test_cli_weather() -> None:
    """Tests inky_pi weather command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["weather", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == f"{WEATHER_ECHO}\n"


def test_cli_goodnight() -> None:
    """Tests inky_pi goodnight command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["night", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == f"{NIGHT_ECHO}\n"


def test_cli_terminal() -> None:
    """Tests inky_pi terminal command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["terminal", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == f"{TERMINAL_ECHO}\n"


def test_cli_desktop() -> None:
    """Tests inky_pi desktop command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["desktop", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == f"{DESKTOP_ECHO}\n"
