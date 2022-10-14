"""Tests for utility methods and classes"""
from unittest.mock import Mock, patch

import pytest

from inky_pi.__main__ import _parse_args, main


def test_can_successfully_parse_args() -> None:
    """Test for parsing arguments"""
    args = _parse_args(["-o", "train", "-m", "inky"])
    assert args.option == "train"
    assert args.output == "inky"


@patch("inky_pi.__main__.import_display")
def test_can_successfully_run_main(display_mock) -> None:
    """Test for running main"""
    args = Mock()
    args.option = "train"
    args.output = "inky"
    with patch("inky_pi.__main__._parse_args", return_value=args):
        main()
        display_mock.assert_called_once()


def test_running_main_with_invalid_args_raises_error() -> None:
    """Test for running main"""
    args = Mock()
    args.option = "invalid"
    args.output = "invalid"
    with patch("inky_pi.__main__._parse_args", return_value=args):
        with pytest.raises(KeyError):
            main()
