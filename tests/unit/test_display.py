"""Tests for display module"""

import platform
from unittest.mock import Mock, patch

import pytest

from inky_pi.configs import InkyColor
from inky_pi.display.display_base import DisplayBase, DisplayModel, DisplayOutput
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

    inky_output = DisplayOutput(
        model=DisplayModel.INKY, base_color=InkyColor.BLACK.value
    )
    import_display(inky_output)
    mock_inky_draw.assert_called_once()
    mock_inky_what.assert_called_once()


def test_instantiating_inky_draw_object_not_on_rpi_raises_import_error() -> None:
    """In on a Raspberry Pi, should be able to instantiate an inky display object;
    but if not, should get an ImportError
    """

    inky_output = DisplayOutput(
        model=DisplayModel.INKY, base_color=InkyColor.BLACK.value
    )
    if platform.machine() == "armv7l":
        ret: DisplayBase = import_display(inky_output)
        assert isinstance(ret, InkyDraw)
    else:
        with pytest.raises(ImportError):
            display_model_factory(inky_output)
        with pytest.raises(SystemExit) as err:
            import_display(inky_output)

        assert err.type == SystemExit
        assert err.value.code == 1


def test_can_successfully_instantiate_terminal_draw_object() -> None:
    """Test for creating terminal instanced object"""

    terminal_object = DisplayOutput(
        model=DisplayModel.TERMINAL, base_color=InkyColor.BLACK.value
    )
    ret: DisplayBase = import_display(terminal_object)
    assert isinstance(ret, TerminalDraw)


def test_can_successfully_instantiate_desktop_draw_object() -> None:
    """Test for creating desktop instanced object"""

    desktop_object = DisplayOutput(
        model=DisplayModel.DESKTOP, base_color=InkyColor.YELLOW.value
    )
    ret: DisplayBase = import_display(desktop_object)
    assert isinstance(ret, InkyDraw)
