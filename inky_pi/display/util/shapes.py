"""Image drawing primitives"""
from typing import Any, Tuple

from PIL import ImageDraw  # type: ignore


def gen_large_sun(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Generate large sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    line_thickness: int = 5
    # Protruding rays
    draw.polygon(
        (
            (x_y[0] + 29, x_y[1]),
            (x_y[0] + 34, x_y[1] + 16),
            (x_y[0] + 24, x_y[1] + 16),
            (x_y[0] + 29, x_y[1]),
        ),
        color,
        line_thickness,
    )  # Top
    draw.polygon(
        (
            (x_y[0] + 29, x_y[1] + 56),
            (x_y[0] + 34, x_y[1] + 46),
            (x_y[0] + 24, x_y[1] + 46),
            (x_y[0] + 29, x_y[1] + 56),
        ),
        color,
        line_thickness,
    )  # Bottom
    draw.polygon(
        (
            (x_y[0], x_y[1] + 28),
            (x_y[0] + 17, x_y[1] + 23),
            (x_y[0] + 17, x_y[1] + 33),
            (x_y[0] + 1, x_y[1] + 28),
        ),
        color,
        line_thickness,
    )  # Left
    draw.polygon(
        (
            (x_y[0] + 57, x_y[1] + 28),
            (x_y[0] + 41, x_y[1] + 23),
            (x_y[0] + 41, x_y[1] + 33),
            (x_y[0] + 57, x_y[1] + 28),
        ),
        color,
        5,
    )  # Right
    draw.line(
        (x_y[0] + 10, x_y[1] + 10, x_y[0] + 47, x_y[1] + 47),
        color,
        line_thickness,
    )
    draw.line(
        (x_y[0] + 10, x_y[1] + 47, x_y[0] + 47, x_y[1] + 10),
        color,
        line_thickness,
    )
    # Sun circle
    draw.ellipse((x_y[0] + 12, x_y[1] + 12, x_y[0] + 45, x_y[1] + 45), color_neg)
    draw.ellipse((x_y[0] + 17, x_y[1] + 17, x_y[0] + 40, x_y[1] + 40), color)


def gen_small_sun(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Generate small sun icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    line_thickness: int = 5
    # Protruding rays
    draw.line((x_y[0] + 5, x_y[1] + 5, x_y[0] + 25, x_y[1] + 25), color, line_thickness)
    draw.line((x_y[0] + 5, x_y[1] + 25, x_y[0] + 25, x_y[1] + 5), color, line_thickness)
    draw.polygon(
        (x_y[0] + 11, x_y[1] + 10, x_y[0], x_y[1] + 15, x_y[0] + 20, x_y[1] + 19),
        color,
    )
    draw.polygon(
        (x_y[0] + 15, x_y[1], x_y[0] + 10, x_y[1] + 10, x_y[0] + 20, x_y[1] + 10),
        color,
    )
    draw.polygon(
        (x_y[0] + 20, x_y[1] + 10, x_y[0] + 30, x_y[1] + 15, x_y[0] + 20, x_y[1] + 20),
        color,
    )
    # Sun circle
    draw.ellipse((x_y[0] + 5, x_y[1] + 5, x_y[0] + 25, x_y[1] + 25), color)
    draw.ellipse((x_y[0] + 10, x_y[1] + 10, x_y[0] + 20, x_y[1] + 20), color_neg)


def gen_large_cloud(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Generate large cloud icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    # Outline
    draw.ellipse((x_y[0], x_y[1] + 20, x_y[0] + 20, x_y[1] + 40), color)
    draw.ellipse((x_y[0] + 5, x_y[1] + 10, x_y[0] + 35, x_y[1] + 40), color)
    draw.ellipse((x_y[0] + 15, x_y[1], x_y[0] + 55, x_y[1] + 40), color)
    draw.ellipse((x_y[0] + 35, x_y[1] + 10, x_y[0] + 65, x_y[1] + 40), color)
    # Negative Space
    draw.ellipse((x_y[0] + 5, x_y[1] + 25, x_y[0] + 15, x_y[1] + 35), color_neg)
    draw.ellipse((x_y[0] + 10, x_y[1] + 15, x_y[0] + 30, x_y[1] + 35), color_neg)
    draw.ellipse((x_y[0] + 20, x_y[1] + 5, x_y[0] + 50, x_y[1] + 35), color_neg)
    draw.ellipse((x_y[0] + 40, x_y[1] + 15, x_y[0] + 60, x_y[1] + 35), color_neg)


def gen_small_cloud(
    draw: ImageDraw, color: Any, color_neg: Any, x_y: Tuple[int, int]
) -> None:
    """Generate small cloud icon

    Args:
        draw: ImageDraw object
        color: Color of the outlines
        color_neg: Color of the negative space
        x_y: (x, y) coordinates
    """
    # Outline
    draw.ellipse((x_y[0], x_y[1] + 10, x_y[0] + 11, x_y[1] + 21), color)
    draw.ellipse((x_y[0] + 5, x_y[1] + 5, x_y[0] + 21, x_y[1] + 21), color)
    draw.ellipse((x_y[0] + 10, x_y[1], x_y[0] + 31, x_y[1] + 21), color)
    draw.ellipse((x_y[0] + 20, x_y[1] + 5, x_y[0] + 36, x_y[1] + 21), color)
    # Negative Space
    draw.ellipse((x_y[0] + 3, x_y[1] + 13, x_y[0] + 8, x_y[1] + 18), color_neg)
    draw.ellipse((x_y[0] + 8, x_y[1] + 8, x_y[0] + 18, x_y[1] + 18), color_neg)
    draw.ellipse((x_y[0] + 13, x_y[1] + 3, x_y[0] + 28, x_y[1] + 18), color_neg)
    draw.ellipse((x_y[0] + 23, x_y[1] + 8, x_y[0] + 33, x_y[1] + 18), color_neg)


def gen_raindrop(draw: ImageDraw, color: Any, x_y: Tuple[int, int]) -> None:
    """Generate raindrop icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_y: (x, y) coordinates
    """
    # Tail
    draw.ellipse((x_y[0] + 3, x_y[1] + 3, x_y[0] + 8, x_y[1] + 7), color)
    # Head
    draw.polygon(
        (
            (x_y[0], x_y[1]),
            (x_y[0] + 6, x_y[1] + 6),
            (x_y[0] + 7, x_y[1] + 3),
            (x_y[0] + 3, x_y[1]),
        ),
        color,
    )


def gen_lightning(draw: ImageDraw, color: Any, x_y: Tuple[int, int]) -> None:
    """Generate lightning bolt icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_y: (x, y) coordinates
    """
    draw.polygon(
        (
            (x_y[0], x_y[1]),
            (x_y[0] + 8, x_y[1]),
            (x_y[0] + 12, x_y[1] + 6),
            (x_y[0] + 6, x_y[1] + 6),
            (x_y[0] + 8, x_y[1] + 12),
            (x_y[0], x_y[1] + 4),
            (x_y[0] + 7, x_y[1] + 4),
            (x_y[0], x_y[1]),
        ),
        color,
    )


def gen_snowflake(draw: ImageDraw, color: Any, x_y: Tuple[int, int]) -> None:
    """Generate snowflake icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_y: (x, y) coordinates
    """
    line_thickness: int = 2
    draw.line((x_y[0] + 5, x_y[1], x_y[0] + 5, x_y[1] + 8), color, line_thickness)
    draw.line((x_y[0] + 1, x_y[1] + 1, x_y[0] + 10, x_y[1] + 6), color, line_thickness)
    draw.line((x_y[0] + 1, x_y[1] + 6, x_y[0] + 10, x_y[1] + 1), color, line_thickness)


def gen_mist(draw: ImageDraw, color: Any, x_y: Tuple[int, int]) -> None:
    """Generate mist icon

    Args:
        draw: ImageDraw object
        color: Color of the object
        x_y: (x, y) coordinates
    """
    line_thickness: int = 4
    draw.line((x_y[0] + 22, x_y[1], x_y[0] + 40, x_y[1]), color, line_thickness)
    draw.line((x_y[0] + 4, x_y[1] + 8, x_y[0] + 47, x_y[1] + 8), color, line_thickness)
    draw.line(
        (x_y[0] + 15, x_y[1] + 16, x_y[0] + 60, x_y[1] + 16),
        color,
        line_thickness,
    )
    draw.line((x_y[0], x_y[1] + 24, x_y[0] + 55, x_y[1] + 24), color, line_thickness)
    draw.line(
        (x_y[0] + 9, x_y[1] + 32, x_y[0] + 51, x_y[1] + 32), color, line_thickness
    )
    draw.line(
        (x_y[0] + 20, x_y[1] + 40, x_y[0] + 40, x_y[1] + 40),
        color,
        line_thickness,
    )
