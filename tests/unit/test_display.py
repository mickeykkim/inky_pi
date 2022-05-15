"""Tests for display module"""
import platform
from unittest.mock import Mock, patch

import pytest

from inky_pi.display.display_base import DisplayBase
from inky_pi.display.terminal_draw import TerminalDraw
from inky_pi.util import DisplayModel, DisplayObject, display_model_factory


@patch("inky_pi.util._import_inky_what")
@patch("inky_pi.util.InkyDraw")
def test_can_successfully_instantiate_inky_draw_object(
    mock_inky_draw: Mock, mock_inky_what: Mock
) -> None:
    """Test for creating InkyDraw instanced object"""

    inky_object = DisplayObject(
        model=DisplayModel.INKY_WHAT,
        base_color="black",
    )
    display_model_factory(inky_object)
    mock_inky_draw.assert_called_once()
    mock_inky_what.assert_called_once()


def test_instantiating_inky_draw_object_not_on_rpi_raises_import_error() -> None:
    """Test for attempting to create InkyDraw instanced object while not on RPI
    raises ImportError
    """

    if platform.machine() != "armv7l":
        inky_object = DisplayObject(
            model=DisplayModel.INKY_WHAT,
            base_color="black",
        )
        with pytest.raises(ImportError):
            display_model_factory(inky_object)


def test_can_successfully_instantiate_terminal_draw_object() -> None:
    """Test for creating terminal instanced object"""

    terminal_object = DisplayObject(
        model=DisplayModel.TERMINAL,
    )
    ret: DisplayBase = display_model_factory(terminal_object)
    assert isinstance(ret, TerminalDraw)
