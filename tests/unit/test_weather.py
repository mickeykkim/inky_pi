"""Tests for weather module"""
import json
from math import isclose
from pathlib import Path
from typing import Generator, Mapping, Union
from unittest.mock import Mock, patch

import pytest

from inky_pi.util import WeatherModel, WeatherObject, weather_model_factory
from inky_pi.weather.open_weather_map import DEG_C, DEG_F, OpenWeatherMap
from inky_pi.weather.weather_base import (
    IconType,
    ScaleType,
    WeatherBase,
    celsius_to_fahrenheit,
    kelvin_to_celsius,
)
from tests.unit.resources.fakes import FakeRequests

TEST_DIR = Path(__file__).parent
RESOURCES_DIR = TEST_DIR.joinpath("resources")
WEATHER_DATA = RESOURCES_DIR.joinpath("weather_data.json")
INVALID_WEATHER_DATA = RESOURCES_DIR.joinpath("cod401.json")


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_weather_vars() -> Generator[Mapping[str, Union[float, str]], None, None]:
    latitude: float = 51.5085
    longitude: float = -0.1257
    exclude_flags: str = "minutely,hourly"
    weather_api_token: str = "1234567890"
    yield locals()


@pytest.fixture
def _setup_weather_fake_data(
    _setup_weather_vars,
) -> Generator[Mapping, None, None]:
    _requests = FakeRequests()
    with open(WEATHER_DATA, "r", encoding="utf-8") as file:
        weather_data = json.load(file)
        _requests.add_response(weather_data, 200)

    weather_base = OpenWeatherMap()
    weather_base.retrieve_data(
        _requests,
        latitude=_setup_weather_vars["latitude"],
        longitude=_setup_weather_vars["longitude"],
        exclude=_setup_weather_vars["exclude_flags"],
        api_key=_setup_weather_vars["weather_api_token"],
    )
    yield locals()


def test_celsius_to_fahrenheit() -> None:
    """Test for converting celsius to fahrenheit
    Conversion significant to tenths place
    """
    assert isclose(celsius_to_fahrenheit(-51), -59.8)
    assert isclose(celsius_to_fahrenheit(0), 32.0)
    assert isclose(celsius_to_fahrenheit(100), 212.0)
    with pytest.raises(ValueError):
        celsius_to_fahrenheit(-273.16)


def test_kelvin_to_celsius() -> None:
    """Test for converting kelvin to celsius
    Conversion significant to tenths place
    """
    assert isclose(kelvin_to_celsius(0), -273.1)
    assert isclose(kelvin_to_celsius(100), -173.1)
    assert isclose(kelvin_to_celsius(373.15), 100.0)
    with pytest.raises(ValueError):
        kelvin_to_celsius(-1)


@patch("inky_pi.util.requests.get")
def test_can_successfully_instantiate_weather_open_weather_map(
    requests_get_mock: Mock,
    _setup_weather_vars: Mapping,
) -> None:
    """Test for creating OpenWeatherMap instanced object

    Args:
        requests_get_mock: Mock for requests.get
        _setup_weather_vars: Setup weather data
    """
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


def test_retrieving_invalid_weather_data_raises_value_error(
    _setup_weather_vars: Mapping,
) -> None:
    """Test to detect sending an invalid API key response

    Args:
        _setup_weather_vars: Setup weather data
    """
    _invalid_requests = FakeRequests()
    with open(INVALID_WEATHER_DATA, "r", encoding="utf-8") as file:
        weather_data = json.load(file)
        _invalid_requests.add_response(weather_data, 200)

    with pytest.raises(ValueError) as exc_info:
        weather_base = OpenWeatherMap()
        weather_base.retrieve_data(
            _invalid_requests,
            latitude=_setup_weather_vars["latitude"],
            longitude=_setup_weather_vars["longitude"],
            exclude=_setup_weather_vars["exclude_flags"],
            api_key=_setup_weather_vars["weather_api_token"],
        )
        assert "Invalid API Key" in str(exc_info.value)


@pytest.mark.parametrize(
    "day, expected_icon_type",
    [
        (0, IconType.SCATTERED_CLOUDS),
        (1, IconType.CLEAR_SKY),
        (2, IconType.RAIN),
        (3, IconType.BROKEN_CLOUDS),
        (4, IconType.SHOWER_RAIN),
        (5, IconType.THUNDERSTORM),
        (6, IconType.SNOW),
        (7, IconType.MIST),
    ],
)
def test_can_successfully_retrieve_weather_icon(
    day: int,
    expected_icon_type: IconType,
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving weather icons

    Args:
        day: Day of the week
        expected_icon_type: Expected icon type
        _setup_weather_fake_data: Setup fixture
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    assert weather_obj.get_icon(day) == expected_icon_type


@pytest.mark.parametrize(
    "day, condition",
    [
        (0, "light rain"),
        (1, "clear sky"),
        (2, "heavy intensity rain"),
    ],
)
def test_can_successfully_retrieve_condition(
    day: int,
    condition: str,
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving weather conditions

    Args:
        day (int): Day of the week
        condition (str): Expected condition
        _setup_weather_fake_data (Mapping): Fixture for weather data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    assert weather_obj.get_condition(day) == condition


@pytest.mark.parametrize(
    "day",
    [-1, 8],
)
def test_retrieving_invalid_day_condition_raises_value_error(
    day: int,
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for that retrieving invalid day condition raises ValueError

    Args:
        day (int): Day of the week
        _setup_weather_fake_data (Mapping): Fixture for weather data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    with pytest.raises(ValueError):
        weather_obj.get_condition(day)


def test_can_successfully_retrieve_current_condition(
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving current condition

    Args:
        _setup_weather_fake_data: Setup weather fake data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    current_condition = "Clouds"
    assert weather_obj.get_current_condition() == current_condition


def test_can_successfully_retrieve_current_weather(
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving current weather

    Args:
        _setup_weather_fake_data: Setup weather data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    current_temp = 289.46
    current_condition = "Clouds"
    expected_string_c = (
        f"{kelvin_to_celsius(current_temp)}{DEG_C} - {current_condition}"
    )
    expected_string_f = (
        f"{celsius_to_fahrenheit(kelvin_to_celsius(current_temp))}"
        f"{DEG_F} - {current_condition}"
    )
    assert weather_obj.get_current_weather() == expected_string_c
    assert weather_obj.get_current_weather(ScaleType.FAHRENHEIT) == expected_string_f


@pytest.mark.parametrize(
    "day, min_k, max_k",
    [
        (0, 284.4, 294.12),
        (1, 287.11, 293.79),
        (2, 284.23, 288.42),
    ],
)
def test_can_successfully_retrieve_temp_range(
    day: int,
    min_k: float,
    max_k: float,
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving temp ranges

    Args:
        day (int): Day of the week
        min_k (float): Minimum temperature in Kelvin
        max_k (float): Maximum temperature in Kelvin
        _setup_weather_fake_data (Mapping): Setup weather data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    min_c = str(kelvin_to_celsius(min_k)) + DEG_C
    max_c = str(kelvin_to_celsius(max_k)) + DEG_C
    min_f = str(celsius_to_fahrenheit(kelvin_to_celsius(min_k))) + DEG_F
    max_f = str(celsius_to_fahrenheit(kelvin_to_celsius(max_k))) + DEG_F
    assert weather_obj.get_temp_range(day) == f"{min_c} – {max_c}"
    assert weather_obj.get_temp_range(day, ScaleType.FAHRENHEIT) == f"{min_f} – {max_f}"


@pytest.mark.parametrize(
    "day, temp_k",
    [
        (0, 292.73),
        (1, 292.95),
        (2, 286.9),
    ],
)
def test_can_successfully_retrieve_future_weather(
    day: int,
    temp_k: float,
    _setup_weather_fake_data: Mapping,
) -> None:
    """Test for retrieving future weather

    Args:
        day (int): Day of the week
        temp_k (float): Temperature in Kelvin
        _setup_weather_fake_data (Mapping): Setup weather data
    """
    weather_obj = _setup_weather_fake_data["weather_base"]
    temp_c = str(kelvin_to_celsius(temp_k)) + DEG_C
    temp_f = str(celsius_to_fahrenheit(kelvin_to_celsius(temp_k))) + DEG_F
    assert weather_obj.get_future_weather(day) == temp_c
    assert weather_obj.get_future_weather(day, ScaleType.FAHRENHEIT) == temp_f
