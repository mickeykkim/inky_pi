"""Inky_Pi weather model module.

Fetches data from OpenWeatherMap API and generates formatted data"""
from typing import Any, Dict, Union

import requests
from loguru import logger

from inky_pi.weather.weather_base import (
    IconType,
    ScaleType,
    WeatherBase,
    WeatherObject,
    celsius_to_fahrenheit,
    kelvin_to_celsius,
)

# Weather formatting constants
DEG_C: str = "\N{DEGREE SIGN}" + "C"
DEG_F: str = "\N{DEGREE SIGN}" + "F"


def _check_day_limit(day: int) -> None:
    if day < 0 or day >= 8:
        logger.error("Invalid day requested", day)
        raise ValueError(
            "Weather data only available for 0 (today) or up to 7 days ahead."
        )


class OpenWeatherMap(WeatherBase):
    """Fetch and manage weather data"""

    def __init__(self) -> None:
        """Initialize variables"""
        self._data: dict = {}

    def retrieve_data(self, protocol: Any, weather_object: WeatherObject) -> None:
        """Retrieves weather data from OpenWeatherMap 7-day forecast API.
        This must be called before any other data manipulation methods.

        Args:
            protocol (Any): Requests object
            weather_object: WeatherObject object
        """
        payload: Dict[str, Union[float, str]] = {
            "lat": weather_object.latitude,
            "lon": weather_object.longitude,
            "exclude": weather_object.exclude_flags,
            "appid": weather_object.weather_api_token,
        }
        response: Any = protocol.get(
            "https://api.openweathermap.org/data/2.5/onecall?", params=payload
        )

        self._data = response.json()

        # Check for errors in weather response, i.e. API key invalid (cod==401)
        if "cod" in self._data:
            err_message: str = self._data["message"]
            logger.warning("Error in weather response", err_message)
            raise ValueError(err_message)

    def get_icon(self, day: int = 0) -> IconType:
        """Retrieves weather type from current OpenWeatherMap weather icon

        Full list of icons/codes: https://openweathermap.org/weather-conditions

        Args:
            day (int): Desired day number (0/today or 1..7)

        Returns:
            IconType: Weather IconType
        """
        _check_day_limit(day)
        icon_code: str = ""
        # Get first 2 code characters; 3rd character is 'd/n' for day/night (ignored)
        if day == 0:
            icon_code = str(self._data["current"]["weather"][0]["icon"])[0:2]
        else:
            icon_code = str(self._data["daily"][day]["weather"][0]["icon"])[0:2]

        weather_type_dict: Dict[str, IconType] = {
            "01": IconType.CLEAR_SKY,
            "02": IconType.FEW_CLOUDS,
            "03": IconType.SCATTERED_CLOUDS,
            "04": IconType.BROKEN_CLOUDS,
            "09": IconType.SHOWER_RAIN,
            "10": IconType.RAIN,
            "11": IconType.THUNDERSTORM,
            "13": IconType.SNOW,
            "50": IconType.MIST,
        }
        return weather_type_dict[icon_code]

    def get_current_weather(self, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Generate current weather string

        String is returned in format:
            [XX.X]°[C/F] - [Current Weather]

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        return f"{self.get_current_temperature(scale)} - {self.get_current_condition()}"

    def get_current_temperature(self, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Generate current temperature

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted temperature string or error message
        """
        try:
            celsius_temp: float = kelvin_to_celsius(
                float(self._data["current"]["temp"])
            )
            formatted_temp: str = (
                str(celsius_temp) + DEG_C
                if scale == ScaleType.CELSIUS
                else str(celsius_to_fahrenheit(celsius_temp)) + DEG_F
            )
            return f"{formatted_temp}"
        except (KeyError, IndexError) as ex:
            logger.error("Invalid get_current_weather data", repr(ex))
            return f"Error retrieving temperature. {ex!r}"

    def get_current_condition(self) -> str:
        """Generate current weather condition

        Returns:
            str: Condition or error message
        """
        try:
            str_status: str = self._data["current"]["weather"][0]["main"]
            return str_status
        except (KeyError, IndexError) as ex:
            logger.error("Invalid get_current_weather data", repr(ex))
            return f"Error retrieving condition. {ex!r}"

    def get_temp_range(self, day: int, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Generate temperature range string

        String is returned in format:
            [XX.X(min)]°[C/F] – [XX.X(max)]°[C/F]

        Args:
            day (int): Desired day number (0/today or 1/tomorrow)
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        _check_day_limit(day)
        try:
            celsius_temp_min: float = kelvin_to_celsius(
                float(self._data["daily"][day]["temp"]["min"])
            )
            celsius_temp_max: float = kelvin_to_celsius(
                float(self._data["daily"][day]["temp"]["max"])
            )
            str_temp_min: str = (
                str(celsius_temp_min) + DEG_C
                if scale == ScaleType.CELSIUS
                else str(celsius_to_fahrenheit(celsius_temp_min)) + DEG_F
            )
            str_temp_max: str = (
                str(celsius_temp_max) + DEG_C
                if scale == ScaleType.CELSIUS
                else str(celsius_to_fahrenheit(celsius_temp_max)) + DEG_F
            )
            return f"{str_temp_min} – {str_temp_max}"
        except (KeyError, IndexError) as ex:
            logger.error("Invalid get_temp_range data", repr(ex))
            return f"Error retrieving range. {ex!r}"

    def get_condition(self, day: int) -> str:
        """Generate weather condition string

        Args:
            day (int): Desired day number (0/today or 1/tomorrow)

        Returns:
            str: Formatted string or error message
        """
        _check_day_limit(day)
        try:
            return f"{self._data['daily'][day]['weather'][0]['description']}"

        except (KeyError, IndexError) as ex:
            logger.error("Invalid fetch_condition data", repr(ex))
            return f"Error retrieving condition. {ex!r}"

    def get_future_weather(self, day: int, scale: ScaleType = ScaleType.CELSIUS) -> str:
        """Generate weather string for given day

        String is returned in format:
            [XX.X]°[C/F]

        Args:
            day (int): Desired day number (0/today or 1..7)
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        _check_day_limit(day)
        try:
            celsius_temp: float = kelvin_to_celsius(
                float(self._data["daily"][day]["temp"]["day"])
            )
            str_temp: str = (
                str(celsius_temp) + DEG_C
                if scale == ScaleType.CELSIUS
                else str(celsius_to_fahrenheit(celsius_temp)) + DEG_F
            )
            return f"{str_temp}"
        except (KeyError, IndexError) as ex:
            logger.error("Invalid get_current_weather data", repr(ex))
            return f"Error retrieving weather. {ex!r}"


def instantiate_open_weather_map(weather_object: WeatherObject) -> OpenWeatherMap:
    """Open Weather Map object creator

    Args:
        weather_object (WeatherObject): weather object containing model

    Returns:
        OpenWeatherMap: OpenWeatherMap object
    """
    weather_base = OpenWeatherMap()
    weather_base.retrieve_data(requests, weather_object)
    return weather_base
