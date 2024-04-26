"""Utility functions for inky_pi."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

from loguru import logger

from inky_pi.display.display_base import DisplayBase, DisplayModel, DisplayOutput
from inky_pi.display.inky_draw import instantiate_inky_display
from inky_pi.display.terminal_draw import instantiate_terminal_display
from inky_pi.train.huxley2 import instantiate_huxley2
from inky_pi.train.open_live import instantiate_open_live
from inky_pi.train.train_base import TrainBase, TrainModel, TrainObject
from inky_pi.weather.open_weather_map import instantiate_open_weather_map
from inky_pi.weather.weather_base import WeatherBase, WeatherModel, WeatherObject

LOG_ROOT_DIR = Path(__file__).parent.parent
LOG_FILE = LOG_ROOT_DIR.joinpath("inky.log")
LOG_ROTATION = "5 MB"
LOG_SERIALIZE = True


def configure_logging() -> None:
    """Configure logging options

    See: https://loguru.readthedocs.io/en/stable/api.html
    """
    logger.add(LOG_FILE, rotation=LOG_ROTATION, serialize=LOG_SERIALIZE)


def display_model_factory(display_object: DisplayOutput) -> DisplayBase:
    """Selects and instantiates the defined display model to use

    Args:
        display_object (DisplayOutput): display object containing model

    Returns:
        DisplayBase: DisplayBase object
    """
    display_handler: dict[DisplayModel, Callable[[DisplayOutput], DisplayBase]] = {
        DisplayModel.INKY: instantiate_inky_display,
        DisplayModel.TERMINAL: instantiate_terminal_display,
        DisplayModel.DESKTOP: instantiate_inky_display,
    }
    return display_handler[display_object.model](display_object)


def import_display(display_object: DisplayOutput) -> DisplayBase:
    """
    Imports the display model from the given display object and returns it.
    On error, logs and exits program (typically if not running on RPi).

    Args:
        display_object (DisplayOutput): The display object to be imported.

    Returns:
        DisplayBase: The display model.
    """
    try:
        return display_model_factory(display_object)
    except ImportError as exc:
        logger.error(exc)
        sys.exit(1)


def _check_open_live_params(train_object: TrainObject) -> None:
    """Checks if the Open Live URL and API token have been provided

    Args:
        train_object (TrainObject): train object containing model

    Raises:
        ValueError: If the Open Live API token is invalid
    """
    if train_object.model != TrainModel.OPEN_LIVE:
        return
    if train_object.url == "" or train_object.token == "":  # nosec B105
        raise ValueError("Open Live requires URL and API token.")


def train_model_factory(train_object: TrainObject) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        TrainBase: TrainBase object
    """
    _check_open_live_params(train_object)
    train_handler: dict[TrainModel, Callable[[TrainObject], TrainBase]] = {
        TrainModel.OPEN_LIVE: instantiate_open_live,
        TrainModel.HUXLEY2: instantiate_huxley2,
    }
    try:
        return train_handler[train_object.model](train_object)
    except ValueError as exc:
        logger.error(exc)
        sys.exit(1)


def weather_model_factory(weather_object: WeatherObject) -> WeatherBase:
    """Selects and instantiates the defined weather model to use

    Args:
        weather_object (WeatherObject): weather object containing model

    Returns:
        WeatherBase: WeatherBase object
    """
    weather_handler: dict[WeatherModel, Callable[[WeatherObject], WeatherBase]] = {
        WeatherModel.OPEN_WEATHER_MAP: instantiate_open_weather_map,
    }
    try:
        return weather_handler[weather_object.model](weather_object)
    except ValueError as exc:
        logger.error(exc)
        sys.exit(1)


def load_json(json_file: Path | str) -> Any:
    """
    Read a Json file and return it

    Args:
        json_file (Path | str): Path to the json file

    Returns:
        Any: Dictionary of station names and their CRS codes
    """
    with open(json_file, "r", encoding="utf-8") as file:
        return json.load(file)
