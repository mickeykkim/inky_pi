"""Tests for weather module"""
from math import isclose
from typing import Generator, Mapping, Union
from unittest.mock import Mock, patch

import pytest

from inky_pi.util import WeatherModel, WeatherObject, weather_model_factory
from inky_pi.weather.open_weather_map import OpenWeatherMap
from inky_pi.weather.weather_base import (
    WeatherBase,
    celsius_to_farenheit,
    kelvin_to_celsius,
)


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_weather_vars() -> Generator[Mapping[str, Union[float, str]], None, None]:
    latitude: float = 51.5085
    longitude: float = -0.1257
    exclude_flags: str = "minutely,hourly"
    weather_api_token: str = "1234567890"
    yield locals()


@patch("inky_pi.weather.open_weather_map.requests.get")
def test_can_successfully_instantiate_weather_open_weather_map(
    requests_get_mock: Mock,
    _setup_weather_vars: Mapping[str, Union[float, str]],
) -> None:
    """Test for creating OpenWeatherMap instanced object"""
    weather_object = WeatherObject(
        model=WeatherModel.OPEN_WEATHER_MAP,
        latitude=_setup_weather_vars["latitude"],
        longitude=_setup_weather_vars["longitude"],
        exclude_flags=_setup_weather_vars["exclude_flags"],
        weather_api_token=_setup_weather_vars["weather_api_token"],
    )
    ret: WeatherBase = weather_model_factory(weather_object)
    requests_get_mock.assert_called_once()
    assert isinstance(ret, OpenWeatherMap)


def test_celcius_to_farhenheit() -> None:
    """Test for converting celsius to farenheit
    Conversion significant to tenths place
    """
    assert isclose(celsius_to_farenheit(-51), -59.8)
    assert isclose(celsius_to_farenheit(0), 32.0)
    assert isclose(celsius_to_farenheit(100), 212.0)
    with pytest.raises(ValueError):
        celsius_to_farenheit(-273.16)


def test_kelvin_to_celsius() -> None:
    """Test for converting kelvin to celsius
    Conversion significant to tenths place
    """
    assert isclose(kelvin_to_celsius(0), -273.1)
    assert isclose(kelvin_to_celsius(100), -173.1)
    assert isclose(kelvin_to_celsius(373.15), 100.0)
    with pytest.raises(ValueError):
        kelvin_to_celsius(-1)
