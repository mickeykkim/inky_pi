"""Inky_Pi drawing module.

Draws strings and icons"""
from enum import Enum, auto
from time import strftime
from typing import Callable, Dict

from font_hanken_grotesk import HankenGroteskBold
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

from inky_pi.train.model_t import str_next_train
from inky_pi.weather.model_w import (str_curr_weather, str_today_temp_range,
                                     str_today_weather_cond,
                                     str_tomorrow_weather_cond)

# Inky display constants
I_DISPLAY = InkyWHAT('black')
I_BLACK = I_DISPLAY.BLACK
I_WHITE = I_DISPLAY.WHITE

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)


class IconType(Enum):
    """Enum for Weather Icon types"""
    sun = auto()
    clouds = auto()
    part_cloud = auto()
    rain = auto()


def render_inky(img: 'Image') -> None:
    """Render border, images (w/text) on inky screen and show on display

    Args:
        img (Image): Image object
    """
    I_DISPLAY.set_border(I_BLACK)
    I_DISPLAY.set_image(img)
    I_DISPLAY.show()


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
    draw.text((x_pos, y_pos), str_next_train(data_t, 1), I_BLACK, FONT_S)
    draw.text((x_pos, y_pos + 30), str_next_train(data_t, 2), I_BLACK, FONT_S)
    draw.text((x_pos, y_pos + 60), str_next_train(data_t, 3), I_BLACK, FONT_S)


def draw_weather_text(draw: 'ImageDraw', data_w: dict, in_celsius: bool,
                      x_pos: int, y_pos: int) -> None:
    """Draw all weather text

    Args:
        draw (ImageDraw): ImageDraw object
        data_w (dict): Dictionary data from OpenWeatherMap JSON req.
        x_pos (int): X position offset
        y_pos (int): Y position offset
    """
    draw.text((x_pos, y_pos), str_curr_weather(data_w, in_celsius), I_BLACK,
              FONT_L)
    draw.text((x_pos, y_pos + 45), str_today_temp_range(data_w, in_celsius),
              I_BLACK, FONT_M)
    draw.text((x_pos, y_pos + 75), str_today_weather_cond(data_w), I_BLACK,
              FONT_M)
    draw.text((x_pos, y_pos + 105), str_tomorrow_weather_cond(data_w), I_BLACK,
              FONT_S)


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
