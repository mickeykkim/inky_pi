"""
This script generates test shapes for the weather icons.
"""
from PIL import Image, ImageDraw

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

BLACK = DesktopDisplayDriver.BLACK
WHITE = DesktopDisplayDriver.WHITE
WIDTH = DesktopDisplayDriver.WIDTH // 6
HEIGHT = DesktopDisplayDriver.HEIGHT // 5
TEST_SHAPE_DIR = "test_shapes"


def _draw_test_sun() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_sun_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/sun.png")


def _draw_test_sun_cloud() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_sun_cloud_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/sun_cloud.png")


def _draw_test_cloud() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_cloud_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/cloud.png")


def _draw_test_cloud_lightning() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_cloud_lightning_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/cloud_lightning.png")


def _draw_test_cloud_rain() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_cloud_rain_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/cloud_rain.png")


def _draw_test_cloud_snow() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_cloud_snow_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/cloud_snow.png")


def _draw_test_mist() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_mist_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/mist.png")


def _draw_test_two_clouds() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_two_clouds_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/two_clouds.png")


def _draw_test_sun_cloud_rain() -> None:
    image = Image.new("P", (WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    draw_sun_cloud_rain_icon(draw, BLACK, WHITE, (0, 0))
    image.save(f"{TEST_SHAPE_DIR}/sun_cloud_rain.png")


def _draw_test_closed_eye() -> None:
    image = Image.new(
        "P", (DesktopDisplayDriver.WIDTH, DesktopDisplayDriver.HEIGHT), color="white"
    )
    draw = ImageDraw.Draw(image)
    gen_closed_eye_icon(
        draw, BLACK, (DesktopDisplayDriver.WIDTH // 2, DesktopDisplayDriver.HEIGHT // 2)
    )
    image.save(f"{TEST_SHAPE_DIR}/closed_eye.png")


def main() -> None:
    """
    Generate test shapes for the weather icons.
    """
    _draw_test_sun()
    _draw_test_sun_cloud()
    _draw_test_cloud()
    _draw_test_cloud_lightning()
    _draw_test_cloud_rain()
    _draw_test_cloud_snow()
    _draw_test_mist()
    _draw_test_two_clouds()
    _draw_test_sun_cloud_rain()
    _draw_test_closed_eye()


if __name__ == "__main__":
    main()
