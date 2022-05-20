"""Base class and helper functions for weather model"""
# pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


def kelvin_to_celsius(kelvin_temp: float) -> float:
    """Helper function to convert Kelvin to Celsius to one decimal place"""
    if kelvin_temp < 0:
        raise ValueError("Kelvin temperature cannot be less than 0.")
    return round(kelvin_temp - 273.15, 1)


def celsius_to_fahrenheit(celsius_temp: float) -> float:
    """Helper function to convert Celsius to Fahrenheit to one decimal place"""
    if celsius_temp < -273.15:
        raise ValueError("Celsius temperature cannot be less than -273.15.")
    return round((celsius_temp * 9 / 5) + 32.0, 1)


class WeatherModel(Enum):
    """Enum of weather models"""

    OPEN_WEATHER_MAP = auto()


@dataclass
class WeatherObject:
    """Weather object"""

    model: WeatherModel
    latitude: float
    longitude: float
    exclude_flags: str
    weather_api_token: str


class IconType(Enum):
    """Enum for Weather Icon types"""

    CLEAR_SKY = auto()
    FEW_CLOUDS = auto()
    SCATTERED_CLOUDS = auto()
    BROKEN_CLOUDS = auto()
    SHOWER_RAIN = auto()
    RAIN = auto()
    THUNDERSTORM = auto()
    SNOW = auto()
    MIST = auto()


class ScaleType(Enum):
    """Enum for Weather Scale types"""

    CELSIUS = auto()
    FAHRENHEIT = auto()


class WeatherBase(ABC):
    """Abstract base class for all weather models"""

    @abstractmethod
    def retrieve_data(self, protocol: Any, weather_object: WeatherObject) -> None:
        """Retrieves weather data from API; must be called after constructor

        Args:
            protocol: HTTP data protocol (e.g. requests)
            weather_object: Weather object
        """

    @abstractmethod
    def get_icon(self, day: int = 0) -> IconType:
        """Return requested weather icon

        Args:
            day (int): Desired day number (0/today or 1..7)

        Returns:
            IconType: Weather IconType
        """

    @abstractmethod
    def get_current_weather(self, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Return requested weather data

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_current_temperature(self, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Return requested current temperature

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_current_condition(self) -> str:
        """Return requested current condition

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_temp_range(self, day: int, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Return temperature range string

        Args:
            day (int): Desired day number (0/today or 1..7)
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_condition(self, day: int) -> str:
        """Return weather condition string

        Args:
            day (int): Desired day number (0/today or 1/tomorrow)

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_future_weather(self, day: int, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Return weather string for given day

        Args:
            day (int): Desired day number (0/today or 1..7)
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
