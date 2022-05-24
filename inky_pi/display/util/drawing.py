"""Weather icon drawing functions"""
from typing import Any

from PIL import ImageDraw  # type: ignore

from inky_pi.display.util.shapes import (
    gen_large_cloud,
    gen_large_sun,
    gen_lightning,
    gen_mist,
    gen_raindrop,
    gen_small_cloud,
    gen_small_sun,
    gen_snowflake,
)


def draw_sun_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_sun(draw, color, color_neg, x_pos + 7, y_pos)


def draw_sun_cloud_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw small sun + large cloud icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_small_sun(draw, color, color_neg, x_pos, y_pos)
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos + 5)


def draw_cloud_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large cloud

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos)


def draw_two_clouds_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large cloud + small cloud icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos)
    gen_small_cloud(draw, color, color_neg, x_pos + 30, y_pos + 25)


def draw_cloud_rain_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large cloud + two rain drop icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos)
    gen_raindrop(draw, color, x_pos + 25, y_pos + 45)
    gen_raindrop(draw, color, x_pos + 42, y_pos + 45)


def draw_sun_cloud_rain_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw small sun, large cloud + two rain drop icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_small_sun(draw, color, color_neg, x_pos, y_pos)
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos + 5)
    gen_raindrop(draw, color, x_pos + 25, y_pos + 50)
    gen_raindrop(draw, color, x_pos + 42, y_pos + 50)


def draw_cloud_lightning_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large cloud + lightning bolt icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos)
    gen_lightning(draw, color, x_pos + 30, y_pos + 45)


def draw_cloud_snow_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw large cloud + snowflake icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_large_cloud(draw, color, color_neg, x_pos, y_pos)
    gen_snowflake(draw, color, x_pos + 12, y_pos + 45)
    gen_snowflake(draw, color, x_pos + 26, y_pos + 50)
    gen_snowflake(draw, color, x_pos + 40, y_pos + 45)


# pylint: disable=unused-argument
def draw_mist_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Draw mist icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    gen_mist(draw, color, x_pos + 5, y_pos)
