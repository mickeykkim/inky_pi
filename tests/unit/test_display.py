"""Tests for display module"""
import platform
from unittest.mock import Mock, patch

import pytest

from inky_pi.display.display_base import DisplayBase, DisplayModel, DisplayObject
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.display.terminal_draw import TerminalDraw
from inky_pi.util import display_model_factory, import_display


@patch("inky_pi.display.inky_draw._import_inky_what")
@patch("inky_pi.display.inky_draw.InkyDraw")
def test_can_successfully_instantiate_inky_draw_object(
    mock_inky_draw: Mock, mock_inky_what: Mock
) -> None:
    """Test for creating InkyDraw instanced object

    Args:
        mock_inky_draw: Mock for InkyDraw
        mock_inky_what: Mock for _import_inky_what
    """

    inky_object = DisplayObject(model=DisplayModel.INKY_WHAT, base_color="black")
    import_display(inky_object)
    mock_inky_draw.assert_called_once()
    mock_inky_what.assert_called_once()


def test_instantiating_inky_draw_object_not_on_rpi_raises_import_error() -> None:
    """In on a Raspberry Pi, should be able to instantiate an inky display object;
    but if not, should get an ImportError
    """

    inky_object = DisplayObject(model=DisplayModel.INKY_WHAT, base_color="black")
    if platform.machine() == "armv7l":
        ret: DisplayBase = import_display(inky_object)
        assert isinstance(ret, InkyDraw)
    else:
        with pytest.raises(ImportError):
            display_model_factory(inky_object)
        with pytest.raises(SystemExit) as err:
            import_display(inky_object)
            assert err.type == SystemExit
            assert err.value.code == 1


def test_can_successfully_instantiate_terminal_draw_object() -> None:
    """Test for creating terminal instanced object"""

    terminal_object = DisplayObject(model=DisplayModel.TERMINAL)
    ret: DisplayBase = import_display(terminal_object)
    assert isinstance(ret, TerminalDraw)


def test_can_successfully_instantiate_desktop_draw_object() -> None:
    """Test for creating desktop instanced object"""

    desktop_object = DisplayObject(model=DisplayModel.DESKTOP, base_color="yellow")
    ret: DisplayBase = import_display(desktop_object)
    assert isinstance(ret, InkyDraw)
