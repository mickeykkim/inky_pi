"""Image drawing primitives"""
from typing import Any

from PIL import ImageDraw  # type: ignore


def gen_large_sun(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Generate large sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    line_thickness: int = 5
    # Protruding rays
    draw.polygon(
        (
            x_pos + 29,
            y_pos,
            x_pos + 34,
            y_pos + 16,
            x_pos + 24,
            y_pos + 16,
            x_pos + 29,
            y_pos,
        ),
        color,
        line_thickness,
    )  # Top
    draw.polygon(
        (
            x_pos + 29,
            y_pos + 56,
            x_pos + 34,
            y_pos + 46,
            x_pos + 24,
            y_pos + 46,
            x_pos + 29,
            y_pos + 56,
        ),
        color,
        line_thickness,
    )  # Bottom
    draw.polygon(
        (
            x_pos,
            y_pos + 28,
            x_pos + 17,
            y_pos + 23,
            x_pos + 17,
            y_pos + 33,
            x_pos + 1,
            y_pos + 28,
        ),
        color,
        line_thickness,
    )  # Left
    draw.polygon(
        (
            x_pos + 57,
            y_pos + 28,
            x_pos + 41,
            y_pos + 23,
            x_pos + 41,
            y_pos + 33,
            x_pos + 57,
            y_pos + 28,
        ),
        color,
        5,
    )  # Right
    draw.line(
        (x_pos + 10, y_pos + 10, x_pos + 47, y_pos + 47),
        color,
        line_thickness,
    )
    draw.line(
        (x_pos + 10, y_pos + 47, x_pos + 47, y_pos + 10),
        color,
        line_thickness,
    )
    # Sun circle
    draw.ellipse((x_pos + 12, y_pos + 12, x_pos + 45, y_pos + 45), color_neg)
    draw.ellipse((x_pos + 17, y_pos + 17, x_pos + 40, y_pos + 40), color)


def gen_small_sun(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Generate small sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    line_thickness: int = 5
    # Protruding rays
    draw.line((x_pos + 5, y_pos + 5, x_pos + 25, y_pos + 25), color, line_thickness)
    draw.line((x_pos + 5, y_pos + 25, x_pos + 25, y_pos + 5), color, line_thickness)
    draw.polygon(
        (x_pos + 11, y_pos + 10, x_pos, y_pos + 15, x_pos + 20, y_pos + 19),
        color,
    )
    draw.polygon(
        (x_pos + 15, y_pos, x_pos + 10, y_pos + 10, x_pos + 20, y_pos + 10),
        color,
    )
    draw.polygon(
        (x_pos + 20, y_pos + 10, x_pos + 30, y_pos + 15, x_pos + 20, y_pos + 20),
        color,
    )
    # Sun circle
    draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 25, y_pos + 25), color)
    draw.ellipse((x_pos + 10, y_pos + 10, x_pos + 20, y_pos + 20), color_neg)


def gen_large_cloud(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Generate large cloud icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    # Outline
    draw.ellipse((x_pos, y_pos + 20, x_pos + 20, y_pos + 40), color)
    draw.ellipse((x_pos + 5, y_pos + 10, x_pos + 35, y_pos + 40), color)
    draw.ellipse((x_pos + 15, y_pos, x_pos + 55, y_pos + 40), color)
    draw.ellipse((x_pos + 35, y_pos + 10, x_pos + 65, y_pos + 40), color)
    # Negative Space
    draw.ellipse((x_pos + 5, y_pos + 25, x_pos + 15, y_pos + 35), color_neg)
    draw.ellipse((x_pos + 10, y_pos + 15, x_pos + 30, y_pos + 35), color_neg)
    draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 50, y_pos + 35), color_neg)
    draw.ellipse((x_pos + 40, y_pos + 15, x_pos + 60, y_pos + 35), color_neg)


def gen_small_cloud(
    draw: ImageDraw, color: Any, color_neg: Any, x_pos: int, y_pos: int
) -> None:
    """Generate small cloud icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    # Outline
    draw.ellipse((x_pos, y_pos + 10, x_pos + 11, y_pos + 21), color)
    draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 21, y_pos + 21), color)
    draw.ellipse((x_pos + 10, y_pos, x_pos + 31, y_pos + 21), color)
    draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 36, y_pos + 21), color)
    # Negative Space
    draw.ellipse((x_pos + 3, y_pos + 13, x_pos + 8, y_pos + 18), color_neg)
    draw.ellipse((x_pos + 8, y_pos + 8, x_pos + 18, y_pos + 18), color_neg)
    draw.ellipse((x_pos + 13, y_pos + 3, x_pos + 28, y_pos + 18), color_neg)
    draw.ellipse((x_pos + 23, y_pos + 8, x_pos + 33, y_pos + 18), color_neg)


def gen_raindrop(draw: ImageDraw, color: Any, x_pos: int, y_pos: int) -> None:
    """Generate raindrop icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    # Tail
    draw.ellipse((x_pos + 3, y_pos + 3, x_pos + 8, y_pos + 7), color)
    # Head
    draw.polygon(
        (
            x_pos,
            y_pos,
            x_pos + 6,
            y_pos + 6,
            x_pos + 7,
            y_pos + 3,
            x_pos + 3,
            y_pos,
        ),
        color,
    )


def gen_lightning(draw: ImageDraw, color: Any, x_pos: int, y_pos: int) -> None:
    """Generate lightning bolt icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    draw.polygon(
        (
            (x_pos, y_pos),
            (x_pos + 8, y_pos),
            (x_pos + 12, y_pos + 6),
            (x_pos + 6, y_pos + 6),
            (x_pos + 8, y_pos + 12),
            (x_pos, y_pos + 4),
            (x_pos + 7, y_pos + 4),
            (x_pos, y_pos),
        ),
        color,
    )


def gen_snowflake(draw: ImageDraw, color: Any, x_pos: int, y_pos: int) -> None:
    """Generate snowflake icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    line_thickness: int = 2
    draw.line((x_pos + 5, y_pos, x_pos + 5, y_pos + 8), color, line_thickness)
    draw.line((x_pos + 1, y_pos + 1, x_pos + 10, y_pos + 6), color, line_thickness)
    draw.line((x_pos + 1, y_pos + 6, x_pos + 10, y_pos + 1), color, line_thickness)


def gen_mist(draw: ImageDraw, color: Any, x_pos: int, y_pos: int) -> None:
    """Generate mist icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_pos: X position of the sun
        y_pos: Y position of the sun
    """
    line_thickness: int = 4
    draw.line((x_pos + 22, y_pos, x_pos + 40, y_pos), color, line_thickness)
    draw.line((x_pos + 4, y_pos + 8, x_pos + 47, y_pos + 8), color, line_thickness)
    draw.line(
        (x_pos + 15, y_pos + 16, x_pos + 60, y_pos + 16),
        color,
        line_thickness,
    )
    draw.line((x_pos, y_pos + 24, x_pos + 55, y_pos + 24), color, line_thickness)
    draw.line((x_pos + 9, y_pos + 32, x_pos + 51, y_pos + 32), color, line_thickness)
    draw.line(
        (x_pos + 20, y_pos + 40, x_pos + 40, y_pos + 40),
        color,
        line_thickness,
    )
