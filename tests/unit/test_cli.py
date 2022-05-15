"""Test cli commands"""

from click.testing import CliRunner

from inky_pi.cli import cli


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
    assert result.output == "CLI inky_pi train\n"


def test_cli_weather() -> None:
    """Tests inky_pi weather command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["weather", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == "CLI inky_pi weather\n"


def test_cli_goodnight() -> None:
    """Tests inky_pi goodnight command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["night", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == "CLI inky_pi night\n"


def test_cli_terminal() -> None:
    """Tests inky_pi goodnight command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["terminal", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == "CLI inky_pi terminal\n"
