"""Inky_Pi weather model module.

Fetches data from OpenWeatherMap API and generates formatted data"""
from enum import Enum, auto
from typing import Any, Dict, Union

import requests

# Weather conversion/formatting constants
K_CONV_C = -273.15
DEG_C = u"\N{DEGREE SIGN}" + "C"
DEG_F = u"\N{DEGREE SIGN}" + "F"


class IconType(Enum):
    """Enum for Weather Icon types"""
    sun = auto()
    clouds = auto()
    part_cloud = auto()
    rain = auto()


class ScaleType(Enum):
    """Enum for Weather Scale types"""
    celsius = auto()
    fahrenheit = auto()


class WeatherModel:
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
        payload: Dict[str, Union[int, Any]] = {
            'lat': latitude,
            'lon': longitude,
            'exclude': exclude,
            'appid': api_key
        }
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/onecall?', params=payload)

        self._data = response.json()

        # Check for errors in weather response, i.e. API key invalid (cod==401)
        if 'cod' in self._data:
            raise ValueError(self._data['message'])

    def get_icon(self) -> 'IconType':
        """Retrieves weather type from current OpenWeatherMap weather icon

        Full list of icons/codes: https://openweathermap.org/weather-conditions

        Returns:
            IconType: Weather IconType
        """
        # Get first two code characters
        # Third character is 'd/n' for day/night; !TODO: implement all icons
        icon_code = str(self._data['current']['weather'][0]['icon'])[0:2]
        weather_dict: Dict[str, 'IconType'] = {
            '01': IconType.sun,  # "clear sky"
            '02': IconType.part_cloud,  # "few clouds"
            '03': IconType.clouds,  # "scattered clouds"
            '04': IconType.clouds,  # "broken clouds"
            '09': IconType.rain,  # "shower rain"
            '10': IconType.rain,  # "rain"
            '11': IconType.rain,  # !TODO: implement "thunderstorm"
            '13': IconType.rain,  # !TODO: implement "snow"
            '50': IconType.clouds,  # !TODO: implement "mist"
        }
        return weather_dict[icon_code]

    def current_weather(self, scale: 'ScaleType') -> str:
        """Generate current weather string

        String is returned in format:
            [XX.X]°[C/F] - [Current Weather]

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        try:
            ctemp = "{:.1f}".format(self._data['current']['temp'] + K_CONV_C)
            str_temp = ctemp + DEG_C if scale == ScaleType.celsius else \
                self._convert_farenheit(ctemp) + DEG_F
            str_status = self._data['current']['weather'][0]['main']
            return f'{str_temp} - {str_status}'
        except (KeyError, TypeError, IndexError):
            return "Error retrieving weather"

    def today_temp_range(self, scale: 'ScaleType') -> str:
        """Generate today's temperature range string

        String is returned in format:
            Today: [XX.X min]°[C/F]–[XX.X max]°[C/F]

        Args:
            scale (ScaleType): Celsius or Fahrenheit for formatting

        Returns:
            str: Formatted string or error message
        """
        try:
            ctemp_min = "{:.1f}".format(self._data['daily'][0]['temp']['min'] +
                                        K_CONV_C)
            ctemp_max = "{:.1f}".format(self._data['daily'][0]['temp']['max'] +
                                        K_CONV_C)
            str_temp_min = ctemp_min + DEG_C if scale == ScaleType.celsius \
                else self._convert_farenheit(ctemp_min) + DEG_F
            str_temp_max = ctemp_max + DEG_C if scale == ScaleType.celsius \
                else self._convert_farenheit(ctemp_max) + DEG_F
            return f'Today: {str_temp_min}–{str_temp_max}'
        except (KeyError, TypeError, IndexError):
            return "Error retrieving range"

    def fetch_condition(self, day: int) -> str:
        """Generate weather condition string

        String is returned in format:
            ["•"/Tomorrow:] [weather condition]

        Returns:
            str: Formatted string or error message
        """
        if day == 0:
            prefix = "\u2022 "
        elif day == 1:
            prefix = "Tomorrow: "
        else:
            raise ValueError(
                "Can only get weather conditions for today and tomorrow.")
        try:
            return prefix + self._data['daily'][0]['weather'][0]['description']
        except (KeyError, TypeError, IndexError):
            return "Error retrieving condition"

    def _convert_farenheit(self, c_temp_str: str) -> str:
        """Helper function to convert Celsius string to Farenheit string
        """
        return "{:.1f}".format(float(c_temp_str) * 9 / 5 + 32)
