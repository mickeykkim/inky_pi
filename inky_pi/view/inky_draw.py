"""Inky_Pi drawing module.

Draws strings and icons"""
from time import strftime
from typing import Any, Callable, Dict

from font_hanken_grotesk import HankenGroteskBold  # type: ignore
from PIL import Image, ImageDraw, ImageFont  # type: ignore

from inky_pi.train.t_model import TrainModel  # type: ignore
from inky_pi.weather.w_model import IconType, WeatherModel  # type: ignore

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)


class InkyDraw():
    """Draw text and shapes onto Inky e-ink display"""
    def __init__(self, inky_model: Any) -> None:
        # Create display and image drawing objects
        self._display = inky_model
        self._img = Image.new('P', (self._display.WIDTH, self._display.HEIGHT))
        self._img_draw = ImageDraw.Draw(self._img)
        self._black = self._display.BLACK
        self._white = self._display.WHITE

    def render_screen(self) -> None:
        """Render border, images (w/text) on inky screen and show on display

        Args:
            img (Image): Image object
        """
        self._display.set_border(self._black)
        self._display.set_image(self._img)
        self._display.show()

    def draw_date_text(self, x_pos: int, y_pos: int) -> None:
        """Draw date text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), strftime('%a %d %b %Y'),
                            self._black, FONT_L)

    def draw_time_text(self, x_pos: int, y_pos: int) -> None:
        """Draw time text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), strftime('%H:%M'), self._black,
                            FONT_L)

    def draw_train_text(self, data_t: 'TrainModel', x_pos: int,
                        y_pos: int) -> None:
        """Draw all train text

        Args:
            data_t (TrainModel): TrainModel object
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), data_t.fetch_train(1), self._black,
                            FONT_S)
        self._img_draw.text((x_pos, y_pos + 30), data_t.fetch_train(2),
                            self._black, FONT_S)
        self._img_draw.text((x_pos, y_pos + 60), data_t.fetch_train(3),
                            self._black, FONT_S)

    def draw_weather_text(self, data_w: 'WeatherModel', in_celsius: bool,
                          x_pos: int, y_pos: int) -> None:
        """Draw all weather text

        Args:
            data_w (WeatherModel): WeatherModel object
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), data_w.current_weather(in_celsius),
                            self._black, FONT_L)
        self._img_draw.text((x_pos, y_pos + 45),
                            data_w.today_temp_range(in_celsius), self._black,
                            FONT_M)
        self._img_draw.text((x_pos, y_pos + 75), data_w.fetch_condition(0),
                            self._black, FONT_M)
        self._img_draw.text((x_pos, y_pos + 105), data_w.fetch_condition(1),
                            self._black, FONT_S)

    def draw_weather_icon(self, icon: IconType, x_pos: int,
                          y_pos: int) -> None:
        """Draws specified icon

        Args:
            icon (IconType): Weather IconType to draw
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        draw_icon_dispatcher: Dict['IconType', Callable] = {
            IconType.sun: self.draw_sun_icon,
            IconType.clouds: self.draw_clouds_icon,
            IconType.part_cloud: self.draw_part_cloud_icon,
            IconType.rain: self.draw_cloud_rain_icon,
        }
        draw_icon_dispatcher[icon](x_pos, y_pos)

    def draw_sun_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large sun icon

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_sun(x_pos + 7, y_pos)

    def draw_part_cloud_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large sun + small cloud icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_sun(x_pos + 7, y_pos)
        self._gen_small_cloud(x_pos + 26, y_pos + 31)

    def draw_clouds_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + small cloud icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_small_cloud(x_pos + 30, y_pos + 30)

    def draw_cloud_rain_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + rain drops icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_raindrop(x_pos + 25, y_pos + 45)
        self._gen_raindrop(x_pos + 42, y_pos + 45)

    def _gen_large_sun(self, x_pos: int, y_pos: int) -> None:
        """Generate large sun icon
        """
        # Protruding rays
        self._img_draw.polygon((x_pos + 29, y_pos, x_pos + 34, y_pos + 16,
                                x_pos + 24, y_pos + 16, x_pos + 29, y_pos),
                               self._black, 5)  # Top
        self._img_draw.polygon(
            (x_pos + 29, y_pos + 56, x_pos + 34, y_pos + 46, x_pos + 24,
             y_pos + 46, x_pos + 29, y_pos + 56), self._black, 5)  # Bottom
        self._img_draw.polygon((x_pos, y_pos + 28, x_pos + 17, y_pos + 23,
                                x_pos + 17, y_pos + 33, x_pos + 1, y_pos + 28),
                               self._black, 5)  # Left
        self._img_draw.polygon(
            (x_pos + 57, y_pos + 28, x_pos + 41, y_pos + 23, x_pos + 41,
             y_pos + 33, x_pos + 57, y_pos + 28), self._black, 5)  # Right
        self._img_draw.line((x_pos + 10, y_pos + 10, x_pos + 47, y_pos + 47),
                            self._black, 5)
        self._img_draw.line((x_pos + 10, y_pos + 47, x_pos + 47, y_pos + 10),
                            self._black, 5)
        # Sun circle
        self._img_draw.ellipse(
            (x_pos + 12, y_pos + 12, x_pos + 45, y_pos + 45), self._white)
        self._img_draw.ellipse(
            (x_pos + 17, y_pos + 17, x_pos + 40, y_pos + 40), self._black)

    def _gen_small_sun(self, x_pos: int, y_pos: int) -> None:
        """Generate small sun icon
        """
        self._img_draw.ellipse((x_pos + 3, y_pos + 3, x_pos + 8, y_pos + 7),
                               self._black)
        self._img_draw.polygon((x_pos, y_pos, x_pos + 6, y_pos + 6, x_pos + 7,
                                y_pos + 3, x_pos + 3, y_pos), self._black)

    def _gen_large_cloud(self, x_pos: int, y_pos: int) -> None:
        """Generate large cloud icon
        """
        # Outline
        self._img_draw.ellipse((x_pos, y_pos + 20, x_pos + 20, y_pos + 40),
                               self._black)
        self._img_draw.ellipse((x_pos + 5, y_pos + 10, x_pos + 35, y_pos + 40),
                               self._black)
        self._img_draw.ellipse((x_pos + 15, y_pos, x_pos + 55, y_pos + 40),
                               self._black)
        self._img_draw.ellipse(
            (x_pos + 35, y_pos + 10, x_pos + 65, y_pos + 40), self._black)
        # Negative Space
        self._img_draw.ellipse((x_pos + 5, y_pos + 25, x_pos + 15, y_pos + 35),
                               self._white)
        self._img_draw.ellipse(
            (x_pos + 10, y_pos + 15, x_pos + 30, y_pos + 35), self._white)
        self._img_draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 50, y_pos + 35),
                               self._white)
        self._img_draw.ellipse(
            (x_pos + 40, y_pos + 15, x_pos + 60, y_pos + 35), self._white)

    def _gen_small_cloud(self, x_pos: int, y_pos: int) -> None:
        """Generate small cloud icon
        """
        # Outline
        self._img_draw.ellipse((x_pos, y_pos + 10, x_pos + 11, y_pos + 21),
                               self._black)
        self._img_draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 21, y_pos + 21),
                               self._black)
        self._img_draw.ellipse((x_pos + 10, y_pos, x_pos + 31, y_pos + 21),
                               self._black)
        self._img_draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 36, y_pos + 21),
                               self._black)
        # Negative Space
        self._img_draw.ellipse((x_pos + 3, y_pos + 13, x_pos + 8, y_pos + 18),
                               self._white)
        self._img_draw.ellipse((x_pos + 8, y_pos + 8, x_pos + 18, y_pos + 18),
                               self._white)
        self._img_draw.ellipse((x_pos + 13, y_pos + 3, x_pos + 28, y_pos + 18),
                               self._white)
        self._img_draw.ellipse((x_pos + 23, y_pos + 8, x_pos + 33, y_pos + 18),
                               self._white)

    def _gen_raindrop(self, x_pos: int, y_pos: int) -> None:
        """Generate raindrop icon
        """
        # Tail
        self._img_draw.ellipse((x_pos + 3, y_pos + 3, x_pos + 8, y_pos + 7),
                               self._black)
        # Head
        self._img_draw.polygon((x_pos, y_pos, x_pos + 6, y_pos + 6, x_pos + 7,
                                y_pos + 3, x_pos + 3, y_pos), self._black)
