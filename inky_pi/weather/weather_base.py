"""Base class and helper functionsfor weather model"""
# pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from enum import Enum, auto


def kelvin_to_celsius(kelvin_temp: float) -> float:
    """Helper function to convert Kelvin to Celsius to one decimal place"""
    return round(kelvin_temp - 273.15, 1)


def celsius_to_farenheit(celsius_temp: float) -> float:
    """Helper function to convert Celsius to Farenheit to one decimal place"""
    return round(celsius_temp * 9 / 5 + 32, 1)


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
    def get_icon(self, day: int = 0) -> IconType:
        """Return requested weather icon

        Args:
            day (int): Desired day number (0/today or 1..7)

        Returns:
            IconType: Weather IconType
        """

    @abstractmethod
    def get_current_weather(self, scale: ScaleType) -> str:
        """Return requested weather data

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """

    @abstractmethod
    def get_current_temperature(self, scale: ScaleType) -> str:
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
    def get_temp_range(self, day: int, scale: ScaleType) -> str:
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
    def get_future_weather(self, day: int, scale: ScaleType) -> str:
        """Return weather string for given day

        Args:
            day (int): Desired day number (0/today or 1..7)
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
