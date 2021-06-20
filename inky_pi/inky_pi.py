"""Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from enum import Enum, auto
from time import strftime

import requests
# For some reason the linter can't find this font in the module
# pylint: disable=no-name-in-module
from font_hanken_grotesk import HankenGroteskBold
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

# Inky display constants
I_DISPLAY = InkyWHAT('black')
I_BLACK = I_DISPLAY.BLACK
I_WHITE = I_DISPLAY.WHITE

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)

# Train constants - i.e. Maze Hill to London Bridge, next 3 departing trains
# CRS station codes: https://huxley2.azurewebsites.net/crs/london%20terminals
T_STATION_FROM = 'MZH'
T_STATION_TO = 'LBG'
T_NUM_DEPARTURES = 3

# Weather constants - i.e. lat, lon @London, GB, exclude minutely, hourly data
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


def _gen_next_train(data_t: dict, num: int) -> str:
    """Generate next train string

    String is returned in format:
        [hh:mm] to [Final Destination Station] - [Status]

    Args:
        data_t (dict): Dictionary data from OpenLDBWS train arrivals JSON req.
        num (int): Next train departing number

    Returns:
        str: Formatted string or error message
    """
    try:
        dest_stn = data_t['trainServices'][num -
                                           1]['origin'][0]['locationName']
        # Check if on time ('sta') or cancelled/delayed ('std')
        if 'sta' in data_t['trainServices'][num - 1]:
            train_arrival_t = data_t['trainServices'][num - 1]['sta']
        elif 'std' in data_t['trainServices'][num - 1]:
            train_arrival_t = data_t['trainServices'][num - 1]['std']
        status = data_t['trainServices'][num - 1]['eta']
        return f'{train_arrival_t} to {dest_stn} - {status}'
    except (KeyError, TypeError):
        try:
            # Try to get the error message & line wrap over each line
            line_length = 41
            return str(data_t['nrccMessages'][0]['value'])[(num - 1) *
                                                           line_length:num *
                                                           line_length]
        except (KeyError, TypeError):
            # If getting the error didn't work just return a generic message
            if num == 1:
                return "Error retrieving train data"
            return ""


def _convert_farenheit(c_temp_str: str) -> float:
    """Helper function to convert Celsius string to Farenheit float value

    Args:
        c_temp_str (str): Temperature in Celsius

    Returns:
        float: Temperature in Farenheit to one decimal point
    """
    return "{:.1f}".format(float(c_temp_str) * 9 / 5 + 32)


def _gen_curr_weather(data_w: dict, in_celsius: bool = True) -> str:
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
    except (KeyError, TypeError):
        return "Error retrieving weather"


def _gen_today_temp_range(data_w: dict, in_celsius: bool = True) -> str:
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
    except (KeyError, TypeError):
        return "Error retrieving range"


def _gen_today_weather_cond(data_w: dict) -> str:
    """Generate today's weather condition string

    String is returned in format:
        [weather condition]

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.

    Returns:
        str: Formatted string or error message
    """
    try:
        return data_w['daily'][0]['weather'][0]['description']
    except (KeyError, TypeError):
        return "Error retrieving condition"


def _gen_large_sun(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate large sun

    Args:
        imgd (ImageDraw): ImageDraw object
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


def _gen_small_sun(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate small sun

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.ellipse((x_off + 3, y_off + 3, x_off + 8, y_off + 7), I_BLACK)
    imgd.polygon((x_off, y_off, x_off + 6, y_off + 6, x_off + 7, y_off + 3,
                  x_off + 3, y_off), I_BLACK)


def _gen_large_cloud(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate large cloud

    Args:
        imgd (ImageDraw): ImageDraw object
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


def _gen_small_cloud(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate small cloud

    Args:
        imgd (ImageDraw): ImageDraw object
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


def _gen_raindrop(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Generate rain drop

    Args:
        imgd (ImageDraw): ImageDraw object
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
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    _gen_large_sun(imgd, x_off + 7, y_off)


def draw_part_cloud_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large sun + small cloud icons

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    _gen_large_sun(imgd, x_off + 7, y_off)
    _gen_small_cloud(imgd, x_off + 26, y_off + 31)


def draw_clouds_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large cloud + small cloud icons

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    _gen_large_cloud(imgd, x_off, y_off)
    _gen_small_cloud(imgd, x_off + 30, y_off + 30)


def draw_cloud_rain_icon(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw large cloud + rain drops icons

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    _gen_large_cloud(imgd, x_off, y_off)
    _gen_raindrop(imgd, x_off + 25, y_off + 45)
    _gen_raindrop(imgd, x_off + 42, y_off + 45)


def draw_date_text(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw date text

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.text((x_off, y_off), strftime('%a %d %b %Y'), I_BLACK, FONT_L)


def draw_time_text(imgd: 'ImageDraw', x_off: int, y_off: int) -> None:
    """Draw time text

    Args:
        imgd (ImageDraw): ImageDraw object
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.text((x_off, y_off), strftime('%H:%M'), I_BLACK, FONT_L)


def draw_train_text(imgd: 'ImageDraw', data_t: dict, x_off: int,
                    y_off: int) -> None:
    """Draw all train text

    Args:
        imgd (ImageDraw): ImageDraw object
        data_t (dict): Dictionary data from OpenLDBWS train arrivals JSON req.
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.text((x_off, y_off), _gen_next_train(data_t, 1), I_BLACK, FONT_S)
    imgd.text((x_off, y_off + 30), _gen_next_train(data_t, 2), I_BLACK, FONT_S)
    imgd.text((x_off, y_off + 60), _gen_next_train(data_t, 3), I_BLACK, FONT_S)


def draw_weather_text(imgd: 'ImageDraw', data_w: dict, x_off: int,
                      y_off: int) -> None:
    """Draw all weather text

    Args:
        imgd (ImageDraw): ImageDraw object
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.
        x_off (int): X position offset
        y_off (int): Y position offset
    """
    imgd.text((x_off, y_off), _gen_curr_weather(data_w), I_BLACK, FONT_L)
    imgd.text((x_off, y_off + 50), _gen_today_temp_range(data_w), I_BLACK,
              FONT_M)
    imgd.text((x_off + 10, y_off + 85), _gen_today_weather_cond(data_w),
              I_BLACK, FONT_M)


def get_weather_type(data_w: dict) -> 'IconType':
    """Retrieves weather type from current OpenWeatherMap weather icon

    Full list of icons/codes: https://openweathermap.org/weather-conditions

    Args:
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.

    Returns:
        IconType: Weather IconType
    """
    # Get first two code characters
    # Third character is 'd/n' for day/night; !TODO: implement day/night icons
    weather_code = str(data_w['current']['weather'][0]['icon'])[0:2]
    dispatcher = {
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
    return dispatcher[weather_code]


def draw_weather_icon(imgd: 'ImageDraw', icon: IconType, x_off: int,
                      y_off: int) -> None:
    """Draws specified icon

    Args:
        imgd (ImageDraw): ImageDraw object
        icon (IconType): Weather IconType to draw
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


# Send requests to API endpoints for train and weather data
data_train = get_train_data(T_STATION_FROM, T_STATION_TO, T_NUM_DEPARTURES)
data_weather = get_weather_data(W_LATITUDE, W_LONGITUDE, W_EXCLUDE, W_API_KEY)
# Check for errors in weather response, i.e. API key is invalid (cod == 401)
if 'cod' in data_weather:
    raise ValueError(data_weather['message'])

# Set image drawing objects
img = Image.new('P', (I_DISPLAY.WIDTH, I_DISPLAY.HEIGHT))
draw = ImageDraw.Draw(img)

# Draw text and weather icon
draw_date_text(draw, 10, 10)
draw_time_text(draw, 300, 10)
draw_train_text(draw, data_train, 10, 60)
draw_weather_text(draw, data_weather, 10, 160)
draw_weather_icon(draw, get_weather_type(data_weather), 300, 200)

# Render border, images (w/text) on inky screen and show on display
I_DISPLAY.set_border(I_BLACK)
I_DISPLAY.set_image(img)
I_DISPLAY.show()
