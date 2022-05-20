"""Desktop Display Driver

This class is a drop-in replacement for the Inky library InkyWHAT class.
Images are drawn using Pillow to a desktop window for testing purposes.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw  # type: ignore


class DesktopDisplayDriver:
    """Desktop Display Driver."""

    WIDTH = 400
    HEIGHT = 300
    BORDER_SIZE = 5
    MAX_VAL = 255
    WHITE = (MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL)
    BLACK = (0, 0, 0, MAX_VAL)
    RED = (MAX_VAL, 0, 0, MAX_VAL)
    YELLOW = (MAX_VAL, MAX_VAL, MAX_VAL // 3, MAX_VAL)

    def __init__(self, base_color: str = "") -> None:
        """Initialize display driver.

        Args:
            base_color: base color
        """
        color_matcher: Dict[str, tuple] = {
            "black": self.BLACK,
            "white": self.WHITE,
            "red": self.RED,
            "yellow": self.YELLOW,
        }

        self._black: tuple = self.BLACK
        self._white: tuple = self.WHITE
        self._color: tuple = (
            self.BLACK if base_color == "" else color_matcher[base_color]
        )
        self._img: Optional[Image] = None
        self._img_draw: Optional[ImageDraw] = None

    def set_image(self, image: Any) -> None:
        """Set image

        Args:
            PIL image: image
        """
        self._img = image

    def set_border(self, border_color: Any) -> None:
        """Draw border around the edge (1/2 self.BORDER_SIZE + 1)

        Args:
            border_color: border color (one of self.<COLOR>)
        """
        side_width = self.BORDER_SIZE * 2
        left_width = side_width - 1
        bottom_width = side_width + 1

        if self._img:
            self._img_draw = ImageDraw.Draw(self._img)
            self._img_draw.line(
                (0, 0, 0, self.HEIGHT),  # |
                border_color,
                left_width,
            )
            self._img_draw.line(
                (0, self.HEIGHT, self.WIDTH, self.HEIGHT),  # |_
                border_color,
                bottom_width,
            )
            self._img_draw.line(
                (self.WIDTH, self.HEIGHT, self.WIDTH, 0),  # |_|
                border_color,
                side_width,
            )
            self._img_draw.line(
                (self.WIDTH, 0, 0, 0),  # □
                border_color,
                side_width,
            )

    def show(self) -> None:
        """Show image

        Uses Pillow to display image on desktop.
        """
        if self._img:
            self._img.show()
        else:
            raise RuntimeError("No image to show")
