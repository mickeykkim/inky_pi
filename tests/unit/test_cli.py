"""Test cli commands"""
import pytest
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
    """Tests inky_pi main command outputs expected result"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]" in result.output


@pytest.mark.parametrize(
    "command, expected_output",
    [
        (["train", "--dry-run"], TRAIN_ECHO),
        (["weather", "--dry-run"], WEATHER_ECHO),
        (["night", "--dry-run"], NIGHT_ECHO),
        (["terminal", "--dry-run"], TERMINAL_ECHO),
        (["desktop", "--dry-run"], DESKTOP_ECHO),
    ],
)
def test_cli_args(command, expected_output) -> None:
    """Tests inky_pi command with various args outputs expected result

    Args:
        command (list): command to run
        expected_output (str): expected output
    """
    runner = CliRunner()
    result = runner.invoke(cli, command)
    assert result.exit_code == 0
    assert result.output == f"{expected_output}\n"
