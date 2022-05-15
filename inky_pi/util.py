"""Utility functions for inky_pi."""
import platform
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict

from loguru import logger

from inky_pi.display.display_base import DisplayBase
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.display.terminal_draw import TerminalDraw
from inky_pi.train.huxley2 import Huxley2
from inky_pi.train.open_live import OpenLive
from inky_pi.train.train_base import TrainBase
from inky_pi.weather.open_weather_map import OpenWeatherMap
from inky_pi.weather.weather_base import WeatherBase


class TrainModel(Enum):
    """Enum of train models"""

    HUXLEY2 = auto()
    OPEN_LIVE = auto()


class WeatherModel(Enum):
    """Enum of weather models"""

    OPEN_WEATHER_MAP = auto()


class DisplayModel(Enum):
    """Enum of display models"""

    INKY_WHAT = auto()
    TERMINAL = auto()


@dataclass
class TrainObject:
    """Train object"""

    model: TrainModel
    station_from: str
    station_to: str
    number: int
    url: str = ""
    token: str = ""


@dataclass
class WeatherObject:
    """Weather object"""

    model: WeatherModel
    latitude: float
    longitude: float
    exclude_flags: str
    weather_api_token: str


@dataclass
class DisplayObject:
    """Display object"""

    model: DisplayModel
    base_color: str = ""


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


def import_display(display_object: DisplayObject) -> DisplayBase:
    """
    Imports the display model from the given object and returns it

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


def configure_logging() -> None:
    """Configure logging options

    See: https://loguru.readthedocs.io/en/stable/api.html
    """
    logger.add("inky.log", rotation="5 MB", serialize=True)


def instantiate_huxley2(train_object: TrainObject) -> Huxley2:
    """Huxley2 object creator

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        Huxley2: Huxley2 object
    """
    return Huxley2(
        train_object.station_from, train_object.station_to, train_object.number
    )


def instantiate_open_live(train_object: TrainObject) -> OpenLive:
    """Open Live object creator

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        OpenLive: OpenLive object
    """
    return OpenLive(
        train_object.station_from,
        train_object.station_to,
        train_object.number,
        train_object.url,
        train_object.token,
    )


def instantiate_open_weather_map(weather_object: WeatherObject) -> OpenWeatherMap:
    """Open Weather Map object creator

    Args:
        weather_object (WeatherObject): weather object containing model

    Returns:
        OpenWeatherMap: OpenWeatherMap object
    """
    return OpenWeatherMap(
        weather_object.latitude,
        weather_object.longitude,
        weather_object.exclude_flags,
        weather_object.weather_api_token,
    )


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
    }
    return display_handler[display_object.model](display_object)
