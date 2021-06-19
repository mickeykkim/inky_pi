# -*- coding: utf-8 -*-
"""Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from time import strftime

import requests
from font_hanken_grotesk import HankenGroteskBold
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

# Train constants - Maze Hill to London Bridge, 3 trains
STATION_FROM = 'MZH'
STATION_TO = 'LBG'
ARRIVAL_NUM = 3

# Weather constants - London, GB
LAT = 51.5085
LON = -0.1257
EXCL = 'minutely,hourly'
W_API_KEY = ""  # Keep secret

# Weather conversion/formatting constants
KELVIN_CONV_C = -273.15
DEG_C = u"\N{DEGREE SIGN}" + "C"
DEG_F = u"\N{DEGREE SIGN}" + "F"

# Inky display variables
inky_display = InkyWHAT('black')
IBLACK = inky_display.BLACK
inky_display.set_border(IBLACK)

# Image drawing variables
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# Fonts
FONT_S = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)

# Train, Weather data
response_train = requests.get(
    'https://huxley2.azurewebsites.net/arrivals/'
    f'{STATION_FROM}/from/{STATION_TO}/{ARRIVAL_NUM}')
data_t = response_train.json()
payload_weather = {'lat': LAT, 'lon': LON, 'exclude': EXCL, 'appid': W_API_KEY}
response_weather = requests.get(
    'https://api.openweathermap.org/data/2.5/onecall?', params=payload_weather)
data_w = response_weather.json()


def gen_train_string(data: dict, n: int) -> str:
    """Generate train string

    String is returned in format:
        [n]) [Train Station] - [HH:MM Time]

    Args:
        data (dict): dictionary data from json request
        n (int): Train number

    Returns:
        str: Formatted string
    """
    try:
        str_station = data['trainServices'][n - 1]['origin'][0]['locationName']
        str_train_t = data['trainServices'][n - 1]['sta']
        return f'{str(n)}) {str_station} - {str_train_t}'
    except (KeyError, TypeError):
        return "Error retrieving train data"


def celsius_str_to_farenheit(c_temp: str) -> float:
    """Convert C to F

    Args:
        c_temp (str): String temperature in Celsius

    Returns:
        float: Temperature in Farenheit
    """
    return "{:.1f}".format(float(c_temp) * 9 / 5 + 32)


def gen_curr_weather(data: dict, in_celsius: bool = True) -> str:
    """Generate current weather string

    String is returned in format:
        [XX.X]°[C/F] - [Current Weather]

    Args:
        data (dict): dictionary data from json request
        in_celsius (bool): if True, formats for C; otherwise formats for F

    Returns:
        str: Formatted string
    """
    try:
        temp_C = "{:.1f}".format(data['current']['temp'] + KELVIN_CONV_C)
        str_temp = temp_C + DEG_C if in_celsius else \
            celsius_str_to_farenheit(temp_C) + DEG_F
        str_status = data['current']['weather'][0]['main']
        return f'{str_temp} - {str_status}'
    except (KeyError, TypeError):
        return "Error retrieving weather"


def gen_today_temp_range(data: dict, in_celsius: bool = True) -> str:
    """Generate today's temperature range string

    String is returned in format:
        Today: [XX.X min]°[C/F]–[XX.X max]°[C/F]

    Args:
        data (dict): dictionary data from json request
        in_celsius (bool): if True, formats for C; otherwise formats for F

    Returns:
        str: Formatted string
    """
    try:
        temp_C_min = "{:.1f}".format(data_w['daily'][0]['temp']['min'] +
                                     KELVIN_CONV_C)
        temp_C_max = "{:.1f}".format(data_w['daily'][0]['temp']['max'] +
                                     KELVIN_CONV_C)
        str_temp_min = temp_C_min + DEG_C if in_celsius else \
            celsius_str_to_farenheit(temp_C_min) + DEG_F
        str_temp_max = temp_C_max + DEG_C if in_celsius else \
            celsius_str_to_farenheit(temp_C_max) + DEG_F
        return f'Today: {str_temp_min}–{str_temp_max}'
    except (KeyError, TypeError):
        return "Error retrieving temperature range"


def gen_today_weather_condition(data: dict) -> str:
    """Generate today's weather condition string

    String is returned in format:
        [weather condition]

    Args:
        data (dict): dictionary data from json request

    Returns:
        str: Formatted string
    """
    try:
        return data['daily'][0]['weather'][0]['description']
    except (KeyError, TypeError):
        return "Error retrieving weather conditions"


# Text retrieval and drawing
SX = 10  # X offset
SY = 10  # Y offset

draw.text((SX, SY), strftime('%a %d %b %Y - %H:%M'), IBLACK, FONT_L)
draw.text((SX, SY + 50), gen_train_string(data_t, 1), IBLACK, FONT_S)
draw.text((SX, SY + 80), gen_train_string(data_t, 2), IBLACK, FONT_S)
draw.text((SX, SY + 110), gen_train_string(data_t, 3), IBLACK, FONT_S)
draw.text((SX, SY + 160), gen_curr_weather(data_w), IBLACK, FONT_L)
draw.text((SX, SY + 210), gen_today_temp_range(data_w), IBLACK, FONT_S)
draw.text((SX, SY + 240), gen_today_weather_condition(data_w), IBLACK, FONT_S)

# Inky display image rendering
inky_display.set_image(img)
inky_display.show()
