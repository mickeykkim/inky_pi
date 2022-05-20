"""Utility functions for inky_pi."""
import platform
import sys
from typing import Any, Callable, Dict

from loguru import logger

from inky_pi.display.desktop_driver import DesktopDisplayDriver
from inky_pi.display.display_base import DisplayBase, DisplayModel, DisplayObject
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.display.terminal_draw import TerminalDraw
from inky_pi.train.huxley2 import instantiate_huxley2
from inky_pi.train.open_live import instantiate_open_live
from inky_pi.train.train_base import TrainBase, TrainModel, TrainObject
from inky_pi.weather.open_weather_map import instantiate_open_weather_map
from inky_pi.weather.weather_base import WeatherBase, WeatherModel, WeatherObject


def _import_inky_what() -> Any:
    """This is a wrapper that imports InkyWHAT to allow mocking it in tests.

    Returns:
        InkyWHAT: Raspberry pi InkyWHAT library
    """
    if platform.machine() == "armv7l":
        # pylint: disable=import-outside-toplevel
        from inky import InkyWHAT  # type: ignore

        return InkyWHAT
    raise ImportError("InkyWHAT library unavailable (are you on a Raspberry Pi?)")


def configure_logging() -> None:
    """Configure logging options

    See: https://loguru.readthedocs.io/en/stable/api.html
    """
    logger.add("inky.log", rotation="5 MB", serialize=True)


def import_display(display_object: DisplayObject) -> DisplayBase:
    """
    Imports the display model from the given display object and returns it.
    On error, logs and exits program (typically if not running on RPi).

    Args:
        display_object (DisplayObject): The display object to be imported.

    Returns:
        DisplayBase: The display model.
    """
    try:
        return display_model_factory(display_object)
    except ImportError as exc:
        logger.error(exc)
        sys.exit(1)


def display_model_factory(display_object: DisplayObject) -> DisplayBase:
    """Selects and instantiates the defined display model to use

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        DisplayBase: DisplayBase object
    """
    display_handler: Dict[DisplayModel, Callable[[DisplayObject], DisplayBase]] = {
        DisplayModel.INKY_WHAT: instantiate_inky_display,
        DisplayModel.TERMINAL: instantiate_terminal_display,
        DisplayModel.DESKTOP: instantiate_desktop_display,
    }
    return display_handler[display_object.model](display_object)


def train_model_factory(train_object: TrainObject) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        TrainBase: TrainBase object
    """
    if train_object.model == TrainModel.OPEN_LIVE and (
        train_object.url is None or train_object.token is None
    ):
        raise ValueError("Open Live requires URL and API token.")

    train_handler: Dict[TrainModel, Callable[[TrainObject], TrainBase]] = {
        TrainModel.OPEN_LIVE: instantiate_open_live,
        TrainModel.HUXLEY2: instantiate_huxley2,
    }
    return train_handler[train_object.model](train_object)


def weather_model_factory(weather_object: WeatherObject) -> WeatherBase:
    """Selects and instantiates the defined weather model to use

    Args:
        weather_object (WeatherObject): weather object containing model

    Returns:
        WeatherBase: WeatherBase object
    """
    weather_handler: Dict[WeatherModel, Callable[[WeatherObject], WeatherBase]] = {
        WeatherModel.OPEN_WEATHER_MAP: instantiate_open_weather_map,
    }
    return weather_handler[weather_object.model](weather_object)


def instantiate_inky_display(display_object: DisplayObject) -> InkyDraw:
    """Inky display object creator

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        InkyDraw: InkyDraw object
    """
    inky_what = _import_inky_what()
    return InkyDraw(inky_what(f"{display_object.base_color}"))


def instantiate_terminal_display(display_object: DisplayObject) -> TerminalDraw:
    """Terminal display object creator

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        TerminalDraw: TerminalDraw object
    """
    return TerminalDraw(display_object.base_color)


def instantiate_desktop_display(display_object: DisplayObject) -> InkyDraw:
    """Desktop display object creator for testing purposes

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        TerminalDraw: TerminalDraw object
    """
    return InkyDraw(DesktopDisplayDriver(display_object.base_color))
