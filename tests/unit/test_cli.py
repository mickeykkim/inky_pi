"""Test cli commands"""
import pytest
from click.testing import CliRunner

from inky_pi.__init__ import __version__  # type: ignore
from inky_pi.cli import OUTPUT_PREFIX, cli


def test_cli_main() -> None:
    """Tests inky_pi main command outputs expected result"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]" in result.output


@pytest.mark.parametrize(
    "command, expected_output",
    [
        (
            ["display", "--option", "train", "--output", "terminal", "--dry-run"],
            f"{OUTPUT_PREFIX} DisplayOption.TRAIN DisplayModel.TERMINAL",
        ),
        (
            ["display", "--option", "weather", "--output", "Terminal", "--dry-run"],
            f"{OUTPUT_PREFIX} DisplayOption.WEATHER DisplayModel.TERMINAL",
        ),
        (
            ["display", "--option", "night", "--output", "TERMINAL", "--dry-run"],
            f"{OUTPUT_PREFIX} DisplayOption.NIGHT DisplayModel.TERMINAL",
        ),
        (
            ["display", "--option", "Train", "--output", "inky", "--dry-run"],
            f"{OUTPUT_PREFIX} DisplayOption.TRAIN DisplayModel.INKY_WHAT",
        ),
        (
            ["display", "--option", "TRAIN", "--output", "desktop", "--dry-run"],
            f"{OUTPUT_PREFIX} DisplayOption.TRAIN DisplayModel.DESKTOP",
        ),
        (
            ["display", "--version"],
            f"cli, version {__version__}",
        ),
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
