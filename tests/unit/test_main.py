"""Tests for utility methods and classes"""
from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from inky_pi.__main__ import _parse_args, main


def test_can_successfully_parse_args() -> None:
    """Test for parsing arguments"""
    args = _parse_args(["-o", "train", "-m", "inky"])
    assert args.option == "train"
    assert args.output == "inky"


def test_running_main_with_invalid_args_raises_error() -> None:
    """Test for running main"""
    args = Mock()
    args.option = "invalid"
    args.output = "invalid"
    with patch("inky_pi.__main__._parse_args", return_value=args):
        with pytest.raises(KeyError):
            main()


def test_running_main_with_display_data_exception_raises_exception() -> None:
    """Test for running main"""
    args = Mock()
    args.option = "train"
    args.output = "inky"
    with (
        patch("inky_pi.__main__._parse_args", return_value=args),
        patch("inky_pi.__main__.display_data", side_effect=ValueError),
    ):
        with pytest.raises(ValueError):
            main()
