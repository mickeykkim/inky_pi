"""
This module contains tests for the drawing functions in inky_pi.display.util.drawing.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest
from PIL import Image, ImageChops, ImageDraw

from inky_pi.display.util.desktop_driver import DesktopDisplayDriver
from inky_pi.display.util.drawing import (
    draw_cloud_icon,
    draw_cloud_lightning_icon,
    draw_cloud_rain_icon,
    draw_cloud_snow_icon,
    draw_mist_icon,
    draw_sun_cloud_icon,
    draw_sun_cloud_rain_icon,
    draw_sun_icon,
    draw_two_clouds_icon,
)
from inky_pi.display.util.shapes import gen_closed_eye_icon
from tests.unit.resources.generate_test_shapes import BLACK, HEIGHT, WHITE, WIDTH

TEST_SHAPE_DIR = Path(__file__).parent / "resources" / "test_shapes"


def _diff_images(
    test_image_name: str, expected_image_name: str
) -> tuple[int, int, int, int] | None:
    test_image = Image.open(TEST_SHAPE_DIR / test_image_name)
    expected_image = Image.open(TEST_SHAPE_DIR / expected_image_name)
    diff = ImageChops.difference(test_image, expected_image).getbbox()
    # delete the temporary image
    (TEST_SHAPE_DIR / test_image_name).unlink()
    return diff


@pytest.mark.parametrize(
    "draw_function, expected_image_name",
    [
        (draw_cloud_icon, "cloud.png"),
        (draw_cloud_lightning_icon, "cloud_lightning.png"),
        (draw_cloud_rain_icon, "cloud_rain.png"),
        (draw_cloud_snow_icon, "cloud_snow.png"),
        (draw_mist_icon, "mist.png"),
        (draw_sun_cloud_rain_icon, "sun_cloud_rain.png"),
        (draw_two_clouds_icon, "two_clouds.png"),
        (draw_sun_icon, "sun.png"),
        (draw_sun_cloud_icon, "sun_cloud.png"),
    ],
)
def test_drawing_function_generates_expected_image(
    draw_function: Callable[
        [
            ImageDraw.ImageDraw,
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int],
        ],
        None,
    ],
    expected_image_name: str,
) -> None:
    """
    Test that each drawing function generates the expected image.

    Args:
        draw_function:
        expected_image_name:
    """
    test_image_name = f"test_{expected_image_name}"
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_function(draw, BLACK, WHITE, (0, 0))
    image.save(TEST_SHAPE_DIR / test_image_name)

    assert not _diff_images(test_image_name, expected_image_name)


def test_drawing_closed_eye_generates_expected_image() -> None:
    """
    Test that the closed eye drawing function generates the expected image.
    """
    test_image_name = "test_closed_eye.png"
    image = Image.new(
        "P", (DesktopDisplayDriver.WIDTH, DesktopDisplayDriver.HEIGHT), color="white"
    )
    draw = ImageDraw.Draw(image)
    gen_closed_eye_icon(
        draw, BLACK, (DesktopDisplayDriver.WIDTH // 2, DesktopDisplayDriver.HEIGHT // 2)
    )
    image.save(TEST_SHAPE_DIR / test_image_name)

    assert not _diff_images(test_image_name, "closed_eye.png")
