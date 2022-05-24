"""Weather icon drawing functions"""
from typing import Any, Tuple

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
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_sun(draw, color, color_neg, (x_y[0] + 7, x_y[1]))


def draw_sun_cloud_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw small sun + large cloud icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_small_sun(draw, color, color_neg, x_y)
    gen_large_cloud(draw, color, color_neg, (x_y[0], x_y[1] + 5))


def draw_cloud_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large cloud

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_cloud(draw, color, color_neg, x_y)


def draw_two_clouds_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large cloud + small cloud icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_cloud(draw, color, color_neg, x_y)
    gen_small_cloud(draw, color, color_neg, (x_y[0] + 30, x_y[1] + 25))


def draw_cloud_rain_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large cloud + two rain drop icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_cloud(draw, color, color_neg, x_y)
    gen_raindrop(draw, color, (x_y[0] + 25, x_y[1] + 45))
    gen_raindrop(draw, color, (x_y[0] + 42, x_y[1] + 45))


def draw_sun_cloud_rain_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw small sun, large cloud + two rain drop icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_small_sun(draw, color, color_neg, x_y)
    gen_large_cloud(draw, color, color_neg, (x_y[0], x_y[1] + 5))
    gen_raindrop(draw, color, (x_y[0] + 25, x_y[1] + 50))
    gen_raindrop(draw, color, (x_y[0] + 42, x_y[1] + 50))


def draw_cloud_lightning_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large cloud + lightning bolt icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_cloud(draw, color, color_neg, x_y)
    gen_lightning(draw, color, (x_y[0] + 30, x_y[1] + 45))


def draw_cloud_snow_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw large cloud + snowflake icons

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_large_cloud(draw, color, color_neg, x_y)
    gen_snowflake(draw, color, (x_y[0] + 12, x_y[1] + 45))
    gen_snowflake(draw, color, (x_y[0] + 26, x_y[1] + 50))
    gen_snowflake(draw, color, (x_y[0] + 40, x_y[1] + 45))


# pylint: disable=unused-argument
def draw_mist_icon(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Draw mist icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    gen_mist(draw, color, (x_y[0] + 5, x_y[1]))
