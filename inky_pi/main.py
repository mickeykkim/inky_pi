"""Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from enum import Enum, auto
from time import strftime
from typing import Any, Callable, Dict, Union

import requests
# For some reason the linter can't find this font in the module
# pylint: disable=no-name-in-module
from font_hanken_grotesk import HankenGroteskBold  # type: ignore
from inky import InkyWHAT  # type: ignore
from PIL import Image, ImageDraw, ImageFont  # type: ignore

# Inky display constants
I_DISPLAY = InkyWHAT('black')
I_BLACK = I_DISPLAY.BLACK
I_WHITE = I_DISPLAY.WHITE

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)

# Train constants - i.e. Maze Hill to London Bridge, next 3 departing trains
T_STATION_FROM = 'maze hill'
T_STATION_TO = 'london bridge'
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


def req_train_data(stn_from: str, stn_to: str, num_trains: int) -> dict:
    """Requests train data from huxley2 (OpenLDBWS) train arrivals API endpoint

    Args:
        stn_from (str): From station
        stn_to (str): To station
        num_trains (int): Number of departing trains to request

    Returns:
        dict: Response OpenLDBWS JSON object as dictionary data
    """
    response = requests.get('https://huxley2.azurewebsites.net/departures/'
                            f'{stn_from}/to/{stn_to}/{num_trains}')
    return response.json()


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


def _abbreviate_station_name(station_name: str) -> str:
    """Abbreviate station name by shortening words like street, lane, etc.

    Args:
        station_name (str): Station name

    Returns:
        str: Abbreviated station name
    """
    abbreviation_dict: Dict[str, str] = {
        "Street": "St",
        "Lane": "Ln",
        "Court": "Ct",
        "Road": "Rd",
        "North": "N",
        "South": "S",
        "East": "E",
        "West": "W",
        "Thameslink": "TL",
    }
    for key, value in abbreviation_dict.items():
        station_name = station_name.replace(key, value)

    return station_name


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
        platform = data_t['trainServices'][num - 1]['platform']
        if platform == "None":
            platform = "?"
        train_arrival_t = data_t['trainServices'][num - 1]['std']
        dest_stn = data_t['trainServices'][num -
                                           1]['destination'][0]['locationName']
        abbr_dest_stn = _abbreviate_station_name(dest_stn)
        status = data_t['trainServices'][num - 1]['etd']
        return f'{train_arrival_t} (P{platform}) to {abbr_dest_stn} - {status}'
    except (KeyError, TypeError, IndexError):
        try:
            # Try to get the error message & line wrap over each line
            line_length = 41
            return str(data_t['nrccMessages'][0]['value'])[(num - 1) *
                                                           line_length:num *
                                                           line_length]
        except (KeyError, TypeError, IndexError):
            # If getting the error didn't work just return a generic message
            if num == 1:
                return "Error retrieving train data"
            return ""


def _convert_farenheit(c_temp_str: str) -> str:
    """Helper function to convert Celsius string to Farenheit string

    Args:
        c_temp_str (str): Temperature in Celsius

    Returns:
        str: Temperature in Farenheit to one decimal point
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
    except (KeyError, TypeError, IndexError):
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
    except (KeyError, TypeError, IndexError):
        return "Error retrieving range"


def _gen_today_weather_cond(data_w: dict) -> str:
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


def _gen_tomorrow_weather_cond(data_w: dict) -> str:
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


def _gen_large_sun(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Generate large sun

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    # Protruding rays
    draw.polygon((x_pos + 29, y_pos, x_pos + 34, y_pos + 16, x_pos + 24,
                  y_pos + 16, x_pos + 29, y_pos), I_BLACK, 5)  # Top
    draw.polygon((x_pos + 29, y_pos + 56, x_pos + 34, y_pos + 46, x_pos + 24,
                  y_pos + 46, x_pos + 29, y_pos + 56), I_BLACK, 5)  # Bottom
    draw.polygon((x_pos, y_pos + 28, x_pos + 17, y_pos + 23, x_pos + 17,
                  y_pos + 33, x_pos + 1, y_pos + 28), I_BLACK, 5)  # Left
    draw.polygon((x_pos + 57, y_pos + 28, x_pos + 41, y_pos + 23, x_pos + 41,
                  y_pos + 33, x_pos + 57, y_pos + 28), I_BLACK, 5)  # Right
    draw.line((x_pos + 10, y_pos + 10, x_pos + 47, y_pos + 47), I_BLACK, 5)
    draw.line((x_pos + 10, y_pos + 47, x_pos + 47, y_pos + 10), I_BLACK, 5)
    # Sun circle
    draw.ellipse((x_pos + 12, y_pos + 12, x_pos + 45, y_pos + 45), I_WHITE)
    draw.ellipse((x_pos + 17, y_pos + 17, x_pos + 40, y_pos + 40), I_BLACK)


def _gen_small_sun(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Generate small sun

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.ellipse((x_pos + 3, y_pos + 3, x_pos + 8, y_pos + 7), I_BLACK)
    draw.polygon((x_pos, y_pos, x_pos + 6, y_pos + 6, x_pos + 7, y_pos + 3,
                  x_pos + 3, y_pos), I_BLACK)


def _gen_large_cloud(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Generate large cloud

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    # Outline
    draw.ellipse((x_pos, y_pos + 20, x_pos + 20, y_pos + 40), I_BLACK)
    draw.ellipse((x_pos + 5, y_pos + 10, x_pos + 35, y_pos + 40), I_BLACK)
    draw.ellipse((x_pos + 15, y_pos, x_pos + 55, y_pos + 40), I_BLACK)
    draw.ellipse((x_pos + 35, y_pos + 10, x_pos + 65, y_pos + 40), I_BLACK)
    # Negative Space
    draw.ellipse((x_pos + 5, y_pos + 25, x_pos + 15, y_pos + 35), I_WHITE)
    draw.ellipse((x_pos + 10, y_pos + 15, x_pos + 30, y_pos + 35), I_WHITE)
    draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 50, y_pos + 35), I_WHITE)
    draw.ellipse((x_pos + 40, y_pos + 15, x_pos + 60, y_pos + 35), I_WHITE)


def _gen_small_cloud(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Generate small cloud

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    # Outline
    draw.ellipse((x_pos, y_pos + 10, x_pos + 11, y_pos + 21), I_BLACK)
    draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 21, y_pos + 21), I_BLACK)
    draw.ellipse((x_pos + 10, y_pos, x_pos + 31, y_pos + 21), I_BLACK)
    draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 36, y_pos + 21), I_BLACK)
    # Negative Space
    draw.ellipse((x_pos + 3, y_pos + 13, x_pos + 8, y_pos + 18), I_WHITE)
    draw.ellipse((x_pos + 8, y_pos + 8, x_pos + 18, y_pos + 18), I_WHITE)
    draw.ellipse((x_pos + 13, y_pos + 3, x_pos + 28, y_pos + 18), I_WHITE)
    draw.ellipse((x_pos + 23, y_pos + 8, x_pos + 33, y_pos + 18), I_WHITE)


def _gen_raindrop(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Generate rain drop

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    # Tail
    draw.ellipse((x_pos + 3, y_pos + 3, x_pos + 8, y_pos + 7), I_BLACK)
    # Head
    draw.polygon((x_pos, y_pos, x_pos + 6, y_pos + 6, x_pos + 7, y_pos + 3,
                  x_pos + 3, y_pos), I_BLACK)


def draw_sun_icon(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw large sun icon

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    _gen_large_sun(draw, x_pos + 7, y_pos)


def draw_part_cloud_icon(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw large sun + small cloud icons

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    _gen_large_sun(draw, x_pos + 7, y_pos)
    _gen_small_cloud(draw, x_pos + 26, y_pos + 31)


def draw_clouds_icon(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw large cloud + small cloud icons

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    _gen_large_cloud(draw, x_pos, y_pos)
    _gen_small_cloud(draw, x_pos + 30, y_pos + 30)


def draw_cloud_rain_icon(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw large cloud + rain drops icons

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    _gen_large_cloud(draw, x_pos, y_pos)
    _gen_raindrop(draw, x_pos + 25, y_pos + 45)
    _gen_raindrop(draw, x_pos + 42, y_pos + 45)


def draw_date_text(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw date text

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.text((x_pos, y_pos), strftime('%a %d %b %Y'), I_BLACK, FONT_L)


def draw_time_text(draw: 'ImageDraw', x_pos: int, y_pos: int) -> None:
    """Draw time text

    Args:
        draw (ImageDraw): ImageDraw object
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.text((x_pos, y_pos), strftime('%H:%M'), I_BLACK, FONT_L)


def draw_train_text(draw: 'ImageDraw', data_t: dict, x_pos: int,
                    y_pos: int) -> None:
    """Draw all train text

    Args:
        draw (ImageDraw): ImageDraw object
        data_t (dict): Dictionary data from OpenLDBWS train arrivals JSON req.
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.text((x_pos, y_pos), _gen_next_train(data_t, 1), I_BLACK, FONT_S)
    draw.text((x_pos, y_pos + 30), _gen_next_train(data_t, 2), I_BLACK, FONT_S)
    draw.text((x_pos, y_pos + 60), _gen_next_train(data_t, 3), I_BLACK, FONT_S)


def draw_weather_text(draw: 'ImageDraw', data_w: dict, x_pos: int,
                      y_pos: int) -> None:
    """Draw all weather text

    Args:
        draw (ImageDraw): ImageDraw object
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.text((x_pos, y_pos), _gen_curr_weather(data_w), I_BLACK, FONT_L)
    draw.text((x_pos, y_pos + 45), _gen_today_temp_range(data_w), I_BLACK,
              FONT_M)
    draw.text((x_pos, y_pos + 75), _gen_today_weather_cond(data_w), I_BLACK,
              FONT_M)
    draw.text((x_pos, y_pos + 105), _gen_tomorrow_weather_cond(data_w),
              I_BLACK, FONT_S)


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


def draw_weather_icon(draw: 'ImageDraw', icon: IconType, x_pos: int,
                      y_pos: int) -> None:
    """Draws specified icon

    Args:
        draw (ImageDraw): ImageDraw object
        icon (IconType): Weather IconType to draw
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw_icon_dispatcher: Dict['IconType', Callable] = {
        IconType.sun: draw_sun_icon,
        IconType.clouds: draw_clouds_icon,
        IconType.part_cloud: draw_part_cloud_icon,
        IconType.rain: draw_cloud_rain_icon,
    }
    draw_icon_dispatcher[icon](draw, x_pos, y_pos)


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set train and weather data
    train_data = req_train_data(T_STATION_FROM, T_STATION_TO, T_NUM_DEPARTURES)
    weather_data = req_weather_data(W_LATITUDE, W_LONGITUDE, W_EXCLUDE,
                                    W_API_KEY)
    # Check for errors in weather response, i.e. API key is invalid (cod==401)
    if 'cod' in weather_data:
        raise ValueError(weather_data['message'])

    # Set image drawing variables
    img = Image.new('P', (I_DISPLAY.WIDTH, I_DISPLAY.HEIGHT))
    img_draw = ImageDraw.Draw(img)

    # Draw text and weather icon
    draw_date_text(img_draw, 10, 10)
    draw_time_text(img_draw, 300, 10)
    draw_train_text(img_draw, train_data, 10, 60)
    draw_weather_text(img_draw, weather_data, 10, 160)
    draw_weather_icon(img_draw, get_weather_icon(weather_data), 300, 200)

    # Render border, images (w/text) on inky screen and show on display
    I_DISPLAY.set_border(I_BLACK)
    I_DISPLAY.set_image(img)
    I_DISPLAY.show()


if __name__ == "__main__":
    main()
