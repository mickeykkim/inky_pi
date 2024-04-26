"""Test cli commands"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from inky_pi.__init__ import __version__  # type: ignore
from inky_pi.cli import OUTPUT_PREFIX, cli, main


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
            [f"{OUTPUT_PREFIX}", "train", "terminal", "Dry run:"],
        ),
        (
            ["display", "--option", "weather", "--output", "Terminal", "--dry-run"],
            [f"{OUTPUT_PREFIX}", "weather", "terminal", "Dry run:"],
        ),
        (
            ["display", "--option", "night", "--output", "TERMINAL", "--dry-run"],
            [f"{OUTPUT_PREFIX}", "night", "terminal", "Dry run:"],
        ),
        (
            ["display", "--option", "Train", "--output", "inky", "--dry-run"],
            [f"{OUTPUT_PREFIX}", "train", "inky", "Dry run:"],
        ),
        (
            ["display", "--option", "TRAIN", "--output", "desktop", "--dry-run"],
            [f"{OUTPUT_PREFIX}", "train", "desktop", "Dry run:"],
        ),
        (
            ["display", "--version"],
            ["cli", f"{__version__}"],
        ),
    ],
)
def test_cli_args(command: list[str], expected_output: list[str]) -> None:
    """Tests inky_pi command with various args outputs expected result

    Args:
        command (list): command to run
        expected_output (str): expected output
    """
    runner = CliRunner()
    result = runner.invoke(cli, command)
    assert result.exit_code == 0, f"Command failed to run {command}"
    for output in expected_output:
        assert f"{output}" in result.output


def test_that_main_runs_successfully() -> None:
    """Test that cli.main() runs"""
    with patch(
        "inky_pi.cli.cli",
        return_value=None,
    ) as mock_cli:
        main()
    mock_cli.assert_called_with()
