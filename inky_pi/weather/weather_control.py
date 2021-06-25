"""Inky_Pi weather control module.

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


def req_weather_data(latitude: float, longitude: float, exclude: str,
                     api_key: str) -> dict:
    """Requests weather data from OpenWeatherMap 7-day forecast API endpoint

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
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?',
                            params=payload)
    return response.json()


def get_weather_icon(data_w: dict) -> 'IconType':
    """Retrieves weather type from current OpenWeatherMap weather icon

    Full list of icons/codes: https://openweathermap.org/weather-conditions

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.

    Returns:
        IconType: Weather IconType
    """
    # Get first two code characters
    # Third character is 'd/n' for day/night; !TODO: implement day/night icons
    icon_code = str(data_w['current']['weather'][0]['icon'])[0:2]
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


def gen_curr_weather(data_w: dict, in_celsius: bool = True) -> str:
    """Generate current weather string

    String is returned in format:
        [XX.X]°[C/F] - [Current Weather]

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.
        in_celsius (bool): If True, formats for °C; otherwise formats for °F

    Returns:
        str: Formatted string or error message
    """
    try:
        ctemp = "{:.1f}".format(data_w['current']['temp'] + K_CONV_C)
        str_temp = ctemp + DEG_C if in_celsius else \
            _convert_farenheit(ctemp) + DEG_F
        str_status = data_w['current']['weather'][0]['main']
        return f'{str_temp} - {str_status}'
    except (KeyError, TypeError, IndexError):
        return "Error retrieving weather"


def gen_today_temp_range(data_w: dict, in_celsius: bool = True) -> str:
    """Generate today's temperature range string

    String is returned in format:
        Today: [XX.X min]°[C/F]–[XX.X max]°[C/F]

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.
        in_celsius (bool): If True, formats for °C; otherwise formats for °F

    Returns:
        str: Formatted string or error message
    """
    try:
        ctemp_min = "{:.1f}".format(data_w['daily'][0]['temp']['min'] +
                                    K_CONV_C)
        ctemp_max = "{:.1f}".format(data_w['daily'][0]['temp']['max'] +
                                    K_CONV_C)
        str_temp_min = ctemp_min + DEG_C if in_celsius else \
            _convert_farenheit(ctemp_min) + DEG_F
        str_temp_max = ctemp_max + DEG_C if in_celsius else \
            _convert_farenheit(ctemp_max) + DEG_F
        return f'Today: {str_temp_min}–{str_temp_max}'
    except (KeyError, TypeError, IndexError):
        return "Error retrieving range"


def gen_today_weather_cond(data_w: dict) -> str:
    """Generate today's weather condition string

    String is returned in format:
        • [weather condition]

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.

    Returns:
        str: Formatted string or error message
    """
    try:
        return "\u2022 " + data_w['daily'][0]['weather'][0]['description']
    except (KeyError, TypeError, IndexError):
        return "Error retrieving condition"


def gen_tomorrow_weather_cond(data_w: dict) -> str:
    """Generate tomorrow's weather condition string

    String is returned in format:
        Tomorrow: [weather condition]

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.

    Returns:
        str: Formatted string or error message
    """
    try:
        return "Tomorrow: " + data_w['daily'][1]['weather'][0]['description']
    except (KeyError, TypeError, IndexError):
        return "Error retrieving condition"


def _convert_farenheit(c_temp_str: str) -> str:
    """Helper function to convert Celsius string to Farenheit string

    Args:
        c_temp_str (str): Temperature in Celsius

    Returns:
        str: Temperature in Farenheit to one decimal point
    """
    return "{:.1f}".format(float(c_temp_str) * 9 / 5 + 32)
