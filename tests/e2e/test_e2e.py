"""
Performs end-to-end test with terminal output to check full program functionality.
Actively retrieves data from both weather and train APIs for testing. Tests may fail
if API endpoints are down.
"""
import re
from typing import List
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner, Result

from inky_pi.cli import cli
from inky_pi.display.util.desktop_driver import DesktopDisplayDriver


@pytest.mark.e2e
def test_running_terminal_ui_generates_expected_output() -> None:
    """Runs the full program and checks each test string is present in output"""
    time = r"(\d+(?:\:\d+))"
    temp = r"(\d+(?:\.\d+)?°(C|F))"
    station_abbr = r"\b[A-Z]{3}(?![A-Z])"
    error_type1 = r"There\sare\sno\strain\sservices\sat\sthis\s\w+"
    error_type2 = r"No\strains\sto\s\w+"
    any_error_msg = rf"({error_type1})|({error_type2})"

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
        rf"({time}\s\|\sP\d+\sto\s(\w+\s)+-\s(\w+\s|{time}))|({any_error_msg})",
    ]

    result: Result = CliRunner().invoke(
        cli, ["display", "--option", "train", "--output", "terminal"]
    )
    assert result.exit_code == 0
    for test_regex in test_regex_list:
        assert re.compile(test_regex).search(result.output) is not None


@pytest.mark.e2e
@patch("inky_pi.display.util.desktop_driver.DesktopDisplayDriver.show")
def test_running_desktop_ui_generates_expected_output(image_show_mock: Mock) -> None:
    """Runs the full program and checks image is drawn to desktop window

    Args:
        image_show_mock (Mock): Mock for image show method
    """
    result: Result = CliRunner().invoke(cli, ["display", "--output", "desktop"])
    image_show_mock.assert_called_once()
    assert result.exit_code == 0


@pytest.mark.e2e
@patch("inky_pi.display.util.desktop_driver.DesktopDisplayDriver.show")
@patch("inky_pi.display.inky_draw._import_inky_what")
def test_running_inky_train_ui_generates_expected_output(
    _import_inky_what_mock: Mock,
    image_show_mock: Mock,
) -> None:
    """Runs the full program and checks image is drawn to desktop window

    Args:
        _import_inky_what_mock (Mock): Mock for import inky_what
        image_show_mock (Mock): Mock for image show method
    """
    _import_inky_what_mock.return_value = DesktopDisplayDriver
    result: Result = CliRunner().invoke(
        cli, ["display", "--option", "train", "--output", "desktop"]
    )
    image_show_mock.assert_called_once()
    assert result.exit_code == 0


@pytest.mark.e2e
@patch("inky_pi.display.util.desktop_driver.DesktopDisplayDriver.show")
@patch("inky_pi.display.inky_draw._import_inky_what")
def test_running_inky_weather_ui_generates_expected_output(
    _import_inky_what_mock: Mock,
    image_show_mock: Mock,
) -> None:
    """Runs the full program and checks image is drawn to desktop window

    Args:
        _import_inky_what_mock (Mock): Mock for import inky_what
        image_show_mock (Mock): Mock for image show method
    """
    _import_inky_what_mock.return_value = DesktopDisplayDriver
    result: Result = CliRunner().invoke(
        cli, ["display", "--option", "weather", "--output", "desktop"]
    )
    image_show_mock.assert_called_once()
    assert result.exit_code == 0


@pytest.mark.e2e
@patch("inky_pi.display.util.desktop_driver.DesktopDisplayDriver.show")
@patch("inky_pi.display.inky_draw._import_inky_what")
def test_running_inky_night_ui_generates_expected_output(
    _import_inky_what_mock: Mock,
    image_show_mock: Mock,
) -> None:
    """Runs the full program and checks image is drawn to desktop window

    Args:
        _import_inky_what_mock (Mock): Mock for import inky_what
        image_show_mock (Mock): Mock for image show method
    """
    _import_inky_what_mock.return_value = DesktopDisplayDriver
    result: Result = CliRunner().invoke(
        cli, ["display", "--option", "night", "--output", "desktop"]
    )
    image_show_mock.assert_called_once()
    assert result.exit_code == 0
