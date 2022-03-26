"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional

from inky_pi.train.huxley2 import Huxley2  # type: ignore
from inky_pi.train.open_live import OpenLive  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore
from inky_pi.weather.open_weather_map import OpenWeatherMap  # type: ignore
from inky_pi.weather.weather_base import WeatherBase  # type: ignore


class TrainModel(Enum):
    """Enum of train models"""

    HUXLEY2 = auto()
    OPEN_LIVE = auto()


class WeatherModel(Enum):
    """Enum of weather models"""

    OPEN_WEATHER_MAP = auto()


@dataclass
class TrainObject:
    """Train object"""

    model: TrainModel
    station_from: str
    station_to: str
    number: int
    url: Optional[str] = None
    token: Optional[str] = None


@dataclass
class WeatherObject:
    """Weather object"""

    model: WeatherModel
    latitude: float
    longitude: float
    exclude_flags: str
    weather_api_token: str


def instantiate_huxley2(train_object: TrainObject) -> Huxley2:
    """Huxley2 object creator"""
    return Huxley2(
        train_object.station_from, train_object.station_to, train_object.number
    )


def instantiate_open_live(train_object: TrainObject) -> OpenLive:
    """Open Live object creator"""
    return OpenLive(
        train_object.station_from,
        train_object.station_to,
        train_object.number,
        train_object.url,
        train_object.token,
    )


def instantiate_open_weather_map(weather_object: WeatherObject) -> OpenWeatherMap:
    """Open Weather Map object creator"""
    return OpenWeatherMap(
        weather_object.latitude,
        weather_object.longitude,
        weather_object.exclude_flags,
        weather_object.weather_api_token,
    )


def train_model_factory(train_object: TrainObject) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        train_object (TrainObject): train object containing model
    """
    if train_object.model == TrainModel.OPEN_LIVE and (
        train_object.url is None or train_object.token is None
    ):
        raise ValueError("Open Live requires URL and API token.")

    train_handler: Dict[TrainModel, TrainBase] = {
        TrainModel.OPEN_LIVE: instantiate_open_live,
        TrainModel.HUXLEY2: instantiate_huxley2,
    }
    return train_handler[train_object.model](train_object)


def weather_model_factory(weather_object: WeatherObject) -> WeatherBase:
    """Selects and instantiates the defined weather model to use

    Args:
        weather_object (WeatherObject): weather object containing model
    """
    weather_handler: Dict[WeatherModel, WeatherBase] = {
        WeatherModel.OPEN_WEATHER_MAP: instantiate_open_weather_map,
    }
    return weather_handler[weather_object.model](weather_object)
