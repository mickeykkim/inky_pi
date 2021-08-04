"""Inky_Pi weather model module.

Fetches data from OpenWeatherMap API and generates formatted data"""
from typing import Dict, Union

import requests

from .weather_base import WeatherBase  # type: ignore
from .weather_base import (IconType, ScaleType, celsius_to_farenheit,
                           kelvin_to_celsius)

# Weather formatting constants
DEG_C: str = u"\N{DEGREE SIGN}" + "C"
DEG_F: str = u"\N{DEGREE SIGN}" + "F"


class OpenWeatherMap(WeatherBase):
    """Fetch and manage weather data"""
    def __init__(self, latitude: float, longitude: float, exclude: str,
                 api_key: str) -> None:
        """Requests weather data from OpenWeatherMap 7-day forecast API

        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            exclude (str): Comma-delimited string of request exclusions
            api_key (str): OpenWeatherMap API Key

        Returns:
            dict: Response OpenWeatherMap JSON object as dictionary data
        """
        payload: Dict[str, Union[float, str]] = {
            'lat': latitude,
            'lon': longitude,
            'exclude': exclude,
            'appid': api_key
        }
        response: requests.Response = requests.get(
            'https://api.openweathermap.org/data/2.5/onecall?', params=payload)

        self._data: dict = response.json()

        # Check for errors in weather response, i.e. API key invalid (cod==401)
        if 'cod' in self._data:
            raise ValueError(self._data['message'])

    def get_icon(self) -> IconType:
        """Retrieves weather type from current OpenWeatherMap weather icon

        Full list of icons/codes: https://openweathermap.org/weather-conditions

        Returns:
            IconType: Weather IconType
        """
        # Get first two code characters; third character is 'd/n' for day/night
        icon_code: str = str(self._data['current']['weather'][0]['icon'])[0:2]
        weather_type_dict: Dict[str, IconType] = {
            '01': IconType.clear_sky,
            '02': IconType.few_clouds,
            '03': IconType.scattered_clouds,
            '04': IconType.broken_clouds,
            '09': IconType.shower_rain,
            '10': IconType.rain,
            '11': IconType.thunderstorm,
            '13': IconType.snow,
            '50': IconType.mist,
        }
        return weather_type_dict[icon_code]

    def get_current_weather(self, scale: ScaleType) -> str:
        """Generate current weather string

        String is returned in format:
            [XX.X]°[C/F] - [Current Weather]

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        try:
            celsius_temp: float = kelvin_to_celsius(
                float(self._data['current']['temp']))
            str_temp: str = str(celsius_temp) + DEG_C \
                if scale == ScaleType.celsius \
                else str(celsius_to_farenheit(celsius_temp)) + DEG_F
            str_status: str = self._data['current']['weather'][0]['main']
            return f'{str_temp} - {str_status}'
        except (KeyError, IndexError):
            return "Error retrieving weather."

    def get_today_temp_range(self, scale: ScaleType) -> str:
        """Generate today's temperature range string

        String is returned in format:
            Today: [XX.X(min)]°[C/F]–[XX.X(max)]°[C/F]

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        try:
            celsius_temp_min: float = kelvin_to_celsius(
                float(self._data['daily'][0]['temp']['min']))
            celsius_temp_max: float = kelvin_to_celsius(
                float(self._data['daily'][0]['temp']['max']))
            str_temp_min: str = str(celsius_temp_min) + DEG_C \
                if scale == ScaleType.celsius \
                else str(celsius_to_farenheit(celsius_temp_min)) + DEG_F
            str_temp_max: str = str(celsius_temp_max) + DEG_C \
                if scale == ScaleType.celsius \
                else str(celsius_to_farenheit(celsius_temp_max)) + DEG_F
            return f'Today: {str_temp_min}–{str_temp_max}'
        except (KeyError, IndexError):
            return "Error retrieving range."

    def fetch_condition(self, day: int) -> str:
        """Generate weather condition string

        String is returned in format:
            ["•"/"Tomorrow:"] [weather condition]

        Args:
            day (int): Desired day number (0/today or 1/tomorrow)

        Returns:
            str: Formatted string or error message
        """
        if day < 0 or day > 1:
            raise ValueError(
                "Weather conditions only available for 0/today or 1/tomorrow.")

        prefix: str = '\u2022' if day == 0 else 'Tomorrow:'
        try:
            return (f"{prefix} "
                    f"{self._data['daily'][day]['weather'][0]['description']}")

        except (KeyError, IndexError):
            return "Error retrieving condition."
