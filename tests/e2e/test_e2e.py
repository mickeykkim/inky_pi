"""
Performs end-to-end test with terminal output to check full program functionality.
Actively retrieves data from both weather and train APIs for testing. Tests may fail
if API endpoints are down.
"""
import re

import pytest
from click.testing import CliRunner, Result

from inky_pi.cli import cli


@pytest.fixture
def _setup_result() -> Result:
    result: Result = CliRunner().invoke(cli, ["terminal"])
    yield result


@pytest.mark.parametrize(
    "test_regex_str",
    [
        r"now:\s(-?\d+(?:\.\d+)?\s*°C(?:\s*-\s*-?\d+(?:\.\d+)?\s*°C)?)",
        r"train\sschedule\sfrom\s\b[A-Z]{3}(?![A-Z])\sto\s\b[A-Z]{3}(?![A-Z]):",
    ],
)
def test_can_successfully_run_full_program_in_terminal(
    test_regex_str: str, _setup_result: Result
) -> None:
    """runs the full program, and checks each test string is present in output"""
    assert _setup_result.exit_code == 0
    assert re.compile(test_regex_str).search(_setup_result.output) is not None
