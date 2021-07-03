"""Base class and helper functionsfor weather model"""
from abc import ABC, abstractmethod
from enum import Enum, auto


def kelvin_to_celsius(kelvin_temp: float) -> float:
    """Helper function to convert Kelvin to Celsius to one decimal place
    """
    return round(kelvin_temp - 273.15, 1)


def celsius_to_farenheit(celsius_temp: float) -> float:
    """Helper function to convert Celsius to Farenheit to one decimal place
    """
    return round(celsius_temp * 9 / 5 + 32, 1)


class IconType(Enum):
    """Enum for Weather Icon types"""
    clear_sky = auto()
    few_clouds = auto()
    scattered_clouds = auto()
    broken_clouds = auto()
    shower_rain = auto()
    rain = auto()
    thunderstorm = auto()
    snow = auto()
    mist = auto()


class ScaleType(Enum):
    """Enum for Weather Scale types"""
    celsius = auto()
    fahrenheit = auto()


class WeatherBase(ABC):
    """Abstract base class for all weather models"""
    @abstractmethod
    def get_icon(self) -> IconType:
        """Return requested weather icon"""
        ...

    @abstractmethod
    def get_current_weather(self, scale: ScaleType) -> str:
        """Return requested weather data"""
        ...

    @abstractmethod
    def get_today_temp_range(self, scale: ScaleType) -> str:
        """Return requested temp range"""
        ...

    @abstractmethod
    def fetch_condition(self, day: int) -> str:
        """Return requested weather condition"""
        ...
