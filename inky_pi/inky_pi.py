"""Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from enum import Enum, auto
from time import strftime

import requests
# pylint: disable=no-name-in-module
from font_hanken_grotesk import HankenGroteskBold
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

# Inky display constants
I_DISPLAY = InkyWHAT('black')
I_BLACK = I_DISPLAY.BLACK
I_WHITE = I_DISPLAY.WHITE

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)

# Train constants - i.e. from Maze Hill to London Bridge, 3 trains
T_STATION_FROM = 'MZH'
T_STATION_TO = 'LBG'
T_NUM_ARRIVALS = 3

# Weather constants - i.e. @London, GB, exclude minutely,hourly data
W_LATITUDE = 51.5085
W_LONGITUDE = -0.1257
W_EXCLUDE = 'minutely,hourly'
# Replace the following w/ your OpenWeatherMap API key & keep it secret:
W_API_KEY = ""

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


def get_train_data(stn_from: str, stn_to: str, num_trains: str) -> dict:
    """Get train data from huxley2 (OpenLDBWS) train arrivals API endpoint

    Args:
        stn_from (str): From station
        stn_to (str): To station
        num_trains (str): Number of departing trains to request

    Returns:
        dict: Response OpenLDBWS JSON object as dictionary data
    """
    response = requests.get('https://huxley2.azurewebsites.net/arrivals/'
                            f'{stn_from}/from/{stn_to}/{num_trains}')
    return response.json()


def get_weather_data(latitude: str, longitude: str, exclude: str,
                     api_key: str) -> dict:
    """Get weather data from OpenWeatherMap 7-day forecast API endpoint

    Args:
        latitude (str): Location latitude
        longitude (str): Location longitude
        exclude (str): Comma-delimited string of request exclusions
        api_key (str): OpenWeatherMap API Key

    Returns:
        dict: Response OpenWeatherMap JSON object as dictionary data
    """
    payload = {
        'lat': latitude,
        'lon': longitude,
        'exclude': exclude,
        'appid': api_key
    }
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?',
                            params=payload)
    return response.json()


def gen_next_train(data: dict, num: int) -> str:
    """Generate next train string

    String is returned in format:
        [num]) [Train Station] - [HH:MM Time]

    Args:
        data (dict): Dictionary data from OpenLDBWS train arrivals JSON request
        num (int): Next train number

    Returns:
        str: Formatted string or error message
    """
    try:
        str_station = \
            data['trainServices'][num - 1]['origin'][0]['locationName']
        str_train_t = data['trainServices'][num - 1]['sta']
        return f'{str(num)}) {str_station} - {str_train_t}'
    except (KeyError, TypeError):
        try:
            return str(data['nrccMessages'][0]['value'])[(num - 1) * 33:num *
                                                         33]
        except (KeyError, TypeError):
            if num == 1:
                return "Error retrieving train data"
            return ""


def convert_farenheit(c_temp: str) -> float:
    """Helper function to convert Celsius string to Farenheit float value

    Args:
        c_temp (str): Temperature in Celsius

    Returns:
        float: Temperature in Farenheit to one decimal point
    """
    return "{:.1f}".format(float(c_temp) * 9 / 5 + 32)


def gen_curr_weather(data: dict, in_celsius: bool = True) -> str:
    """Generate current weather string

    String is returned in format:
        [XX.X]°[C/F] - [Current Weather]

    Args:
        data (dict): Dictionary data from OpenWeatherMap JSON request
        in_celsius (bool): If True, formats for C; otherwise formats for F

    Returns:
        str: Formatted string or error message
    """
    try:
        ctemp = "{:.1f}".format(data['current']['temp'] + K_CONV_C)
        str_temp = ctemp + DEG_C if in_celsius else \
            convert_farenheit(ctemp) + DEG_F
        str_status = data['current']['weather'][0]['main']
        return f'{str_temp} - {str_status}'
    except (KeyError, TypeError):
        return "Error retrieving weather"


def gen_today_temp_range(data: dict, in_celsius: bool = True) -> str:
    """Generate today's temperature range string

    String is returned in format:
        Today: [XX.X min]°[C/F]–[XX.X max]°[C/F]

    Args:
        data (dict): Dictionary data from OpenWeatherMap JSON request
        in_celsius (bool): If True, formats for C; otherwise formats for F

    Returns:
        str: Formatted string or error message
    """
    try:
        ctemp_min = "{:.1f}".format(data['daily'][0]['temp']['min'] + K_CONV_C)
        ctemp_max = "{:.1f}".format(data['daily'][0]['temp']['max'] + K_CONV_C)
        str_temp_min = ctemp_min + DEG_C if in_celsius else \
            convert_farenheit(ctemp_min) + DEG_F
        str_temp_max = ctemp_max + DEG_C if in_celsius else \
            convert_farenheit(ctemp_max) + DEG_F
        return f'Today: {str_temp_min}–{str_temp_max}'
    except (KeyError, TypeError):
        return "Error retrieving range"


def gen_today_weather_cond(data: dict) -> str:
    """Generate today's weather condition string

    String is returned in format:
        [weather condition]

    Args:
        data (dict): Dictionary data from OpenWeatherMap JSON request

    Returns:
        str: Formatted string or error message
    """
    try:
        return data['daily'][0]['weather'][0]['description']
    except (KeyError, TypeError):
        return "Error retrieving condition"


def draw_all_text(imgd: 'ImageDraw', data_t: dict, data_w: dict, x_off: int,
                  y_off: int) -> None:
    """Draw all text for train and weather data

    Args:
        imgd ('ImageDraw'): ImageDraw object
        data_t (dict): Dictionary data from OpenLDBWS train arrivals json
        data_w (dict): Dictionary data from openweathermap json
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.text((x_off, y_off), strftime('%a %d %b %Y- %H:%M'), I_BLACK, FONT_L)
    imgd.text((x_off, y_off + 50), gen_next_train(data_t, 1), I_BLACK, FONT_S)
    imgd.text((x_off, y_off + 80), gen_next_train(data_t, 2), I_BLACK, FONT_S)
    imgd.text((x_off, y_off + 110), gen_next_train(data_t, 3), I_BLACK, FONT_S)
    imgd.text((x_off, y_off + 160), gen_curr_weather(data_w), I_BLACK, FONT_L)
    imgd.text((x_off, y_off + 210), gen_today_temp_range(data_w), I_BLACK,
              FONT_S)
    imgd.text((x_off + 10, y_off + 240), gen_today_weather_cond(data_w),
              I_BLACK, FONT_S)


def draw_weather_icon(imgd: 'ImageDraw', icon: IconType, x_off: int,
                      y_off: int) -> None:
    """Draws specified icon

    Args:
        imgd ('ImageDraw'): ImageDraw object
        icon (IconType): icon to draw
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    dispatcher = {
        IconType.sun: draw_sun_icon,
        IconType.clouds: draw_clouds_icon,
        IconType.part_cloud: draw_part_cloud_icon,
        IconType.rain: draw_cloud_rain_icon,
    }
    dispatcher[icon](imgd, x_off, y_off)


def gen_large_sun(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate large sun

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    # Protruding rays
    imgd.polygon((x_off + 29, y_off, x_off + 34, y_off + 16, x_off + 24,
                  y_off + 16, x_off + 29, y_off), I_BLACK, 5)  # Top
    imgd.polygon((x_off + 29, y_off + 56, x_off + 34, y_off + 46, x_off + 24,
                  y_off + 46, x_off + 29, y_off + 56), I_BLACK, 5)  # Bottom
    imgd.polygon((x_off, y_off + 28, x_off + 17, y_off + 23, x_off + 17,
                  y_off + 33, x_off + 1, y_off + 28), I_BLACK, 5)  # Left
    imgd.polygon((x_off + 57, y_off + 28, x_off + 41, y_off + 23, x_off + 41,
                  y_off + 33, x_off + 57, y_off + 28), I_BLACK, 5)  # Right
    imgd.line((x_off + 10, y_off + 10, x_off + 47, y_off + 47), I_BLACK, 5)
    imgd.line((x_off + 10, y_off + 47, x_off + 47, y_off + 10), I_BLACK, 5)
    # Sun circle
    imgd.ellipse((x_off + 12, y_off + 12, x_off + 45, y_off + 45), I_WHITE)
    imgd.ellipse((x_off + 17, y_off + 17, x_off + 40, y_off + 40), I_BLACK)


def gen_small_sun(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate small sun

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.ellipse((x_off + 3, y_off + 3, x_off + 8, y_off + 7), I_BLACK)
    imgd.polygon((x_off, y_off, x_off + 6, y_off + 6, x_off + 7, y_off + 3,
                  x_off + 3, y_off), I_BLACK)


def gen_large_cloud(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate large cloud

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    # Outline
    imgd.ellipse((x_off, y_off + 20, x_off + 20, y_off + 40), I_BLACK)
    imgd.ellipse((x_off + 5, y_off + 10, x_off + 35, y_off + 40), I_BLACK)
    imgd.ellipse((x_off + 15, y_off, x_off + 55, y_off + 40), I_BLACK)
    imgd.ellipse((x_off + 35, y_off + 10, x_off + 65, y_off + 40), I_BLACK)
    # Negative Space
    imgd.ellipse((x_off + 5, y_off + 25, x_off + 15, y_off + 35), I_WHITE)
    imgd.ellipse((x_off + 10, y_off + 15, x_off + 30, y_off + 35), I_WHITE)
    imgd.ellipse((x_off + 20, y_off + 5, x_off + 50, y_off + 35), I_WHITE)
    imgd.ellipse((x_off + 40, y_off + 15, x_off + 60, y_off + 35), I_WHITE)


def gen_small_cloud(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate small cloud

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    # Outline
    imgd.ellipse((x_off, y_off + 10, x_off + 11, y_off + 21), I_BLACK)
    imgd.ellipse((x_off + 5, y_off + 5, x_off + 21, y_off + 21), I_BLACK)
    imgd.ellipse((x_off + 10, y_off, x_off + 31, y_off + 21), I_BLACK)
    imgd.ellipse((x_off + 20, y_off + 5, x_off + 36, y_off + 21), I_BLACK)
    # Negative Space
    imgd.ellipse((x_off + 3, y_off + 13, x_off + 8, y_off + 18), I_WHITE)
    imgd.ellipse((x_off + 8, y_off + 8, x_off + 18, y_off + 18), I_WHITE)
    imgd.ellipse((x_off + 13, y_off + 3, x_off + 28, y_off + 18), I_WHITE)
    imgd.ellipse((x_off + 23, y_off + 8, x_off + 33, y_off + 18), I_WHITE)


def gen_raindrop(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate rain drop

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    # Tail
    imgd.ellipse((x_off + 3, y_off + 3, x_off + 8, y_off + 7), I_BLACK)
    # Head
    imgd.polygon((x_off, y_off, x_off + 6, y_off + 6, x_off + 7, y_off + 3,
                  x_off + 3, y_off), I_BLACK)


def draw_sun_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large sun icon

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    gen_large_sun(imgd, x_off + 7, y_off)


def draw_part_cloud_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large sun + small cloud icons

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    gen_large_sun(imgd, x_off + 7, y_off)
    gen_small_cloud(imgd, x_off + 26, y_off + 31)


def draw_clouds_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large cloud + small cloud icons

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    gen_large_cloud(imgd, x_off, y_off)
    gen_small_cloud(imgd, x_off + 30, y_off + 30)


def draw_cloud_rain_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large cloud + rain drops icons

    Args:
        imgd ('ImageDraw'): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    gen_large_cloud(imgd, x_off, y_off)
    gen_raindrop(imgd, x_off + 25, y_off + 45)
    gen_raindrop(imgd, x_off + 42, y_off + 45)


# Send requests to API endpoints for train and weather data
data_train = get_train_data(T_STATION_FROM, T_STATION_TO, T_NUM_ARRIVALS)
data_weather = get_weather_data(W_LATITUDE, W_LONGITUDE, W_EXCLUDE, W_API_KEY)
# Check for errors in weather response, i.e. API key is invalid (cod == 401)
if 'cod' in data_weather:
    raise ValueError(data_weather['message'])

# Set image drawing objects
img = Image.new('P', (I_DISPLAY.WIDTH, I_DISPLAY.HEIGHT))
draw = ImageDraw.Draw(img)

# Draw text and weather icon
draw_all_text(draw, data_train, data_weather, 10, 10)
w_icon = IconType.rain
draw_weather_icon(draw, w_icon, 300, 200)

# Render border, images (w/text) on inky screen and show on display
I_DISPLAY.set_border(I_BLACK)
I_DISPLAY.set_image(img)
I_DISPLAY.show()
