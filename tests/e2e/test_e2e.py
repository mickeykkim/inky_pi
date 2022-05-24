"""
Performs end-to-end test with terminal output to check full program functionality.
Actively retrieves data from both weather and train APIs for testing. Tests may fail
if API endpoints are down.
"""
import re
from typing import Generator, List

import pytest
from click.testing import CliRunner, Result

from inky_pi.cli import cli


@pytest.fixture
def _setup_result() -> Generator:
    result: Result = CliRunner().invoke(cli, ["terminal"])
    yield result


@pytest.mark.e2e
def test_running_terminal_ui_generates_expected_output(_setup_result: Result) -> None:
    """Runs the full program and checks each test string is present in output

    Args:
        _setup_result (Result): fixture for cli runner
    """
    time = r"(\d+(?:\:\d+))"
    temp = r"(\d+(?:\.\d+)?°(C|F))"
    station_abbr = r"\b[A-Z]{3}(?![A-Z])"
    error_msg = r"(There\sare\sno\strain\sservices\sat\sthis\s)|(Error:\s\w+)"

    test_regex_list: List[str] = [
        # Time (HH:MM)
        rf"{time}",
        # Date (Day dd MMM yyyy)
        r"[A-Z][a-z]{2}\s\d*\s[A-Z][a-z]*\s\d{4}",
        # now: <current>°C/F
        rf"now:\s{temp}",
        # today: <low>°C/F – <high>°C/F
        rf"today:\s{temp}\s–\s{temp}",
        # train schedule from <station> to <station>
        rf"train\sschedule\sfrom\s{station_abbr}\sto\s{station_abbr}:",
        # <HH:MM> | P<#> to <station> - <status> [OR] <error message>
        rf"({time}\s\|\sP\d+\sto\s\w+\s\-\s(\w+\s|{time}))|({error_msg})",
    ]

    assert _setup_result.exit_code == 0
    for test_regex in test_regex_list:
        assert re.compile(test_regex).search(_setup_result.output) is not None
