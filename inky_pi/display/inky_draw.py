"""Inky_Pi drawing module.

Draws strings and icons"""
from time import strftime
from typing import Any, Callable, Dict

# pylint: disable=no-name-in-module
from font_fredoka_one import FredokaOne  # type: ignore
from font_hanken_grotesk import HankenGroteskBold  # type: ignore
from PIL import Image, ImageDraw, ImageFont  # type: ignore

from inky_pi.train.train_base import TrainBase  # type: ignore
from inky_pi.weather.weather_base import IconType  # type: ignore
from inky_pi.weather.weather_base import ScaleType  # type: ignore
from inky_pi.weather.weather_base import WeatherBase  # type: ignore

# Font constants
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)
FONT_GS = ImageFont.truetype(FredokaOne, 25)
FONT_GM = ImageFont.truetype(FredokaOne, 30)
FONT_GL = ImageFont.truetype(FredokaOne, 40)


class InkyDraw():
    """Draw text and shapes onto Inky e-ink display"""

    def __init__(self, inky_model: Any) -> None:
        """Create display and image drawing objects

        Args:
            inky_model (Any): Inky display model (i.e. InkyWHAT('black'))
        """
        self._display: Any = inky_model
        self._img: 'Image' = Image.new('P', (self._display.WIDTH, self._display.HEIGHT))
        self._img_draw: 'ImageDraw' = ImageDraw.Draw(self._img)
        self._black: Any = self._display.BLACK
        self._white: Any = self._display.WHITE
        self._color: Any = self._display.YELLOW

    def render_screen(self) -> None:
        """Render border, images (w/text) on inky screen and show on display
        """
        self._display.set_border(self._black)
        self._display.set_image(self._img)
        self._display.show()

    def draw_goodnight(self, data_w: WeatherBase, scale: 'ScaleType') -> None:
        """Render goodnight screen
        """
        self._draw_goodnight_icon()
        self._draw_goodnight_text(data_w, scale)

    def _draw_goodnight_icon(self):
        x_mid = self._display.WIDTH / 2
        y_mid = self._display.HEIGHT / 2
        # Closed eye icon
        line_width = 8
        x_0, y_0 = x_mid - 75, -50
        x_1, y_1 = x_mid + 75, y_mid - 75
        a_start = 20
        a_end = 160
        self._img_draw.arc([(x_0, y_0), (x_1, y_1)], a_start, a_end, self._color,
                           line_width)
        self._img_draw.line([(x_0 + 9, y_0 + 131), (x_0 + 29, y_0 + 111)], self._color,
                            line_width)
        self._img_draw.line([(x_0 + 49, y_0 + 147), (x_0 + 59, y_0 + 122)], self._color,
                            line_width)
        self._img_draw.line([(x_0 + 104, y_0 + 147), (x_0 + 94, y_0 + 122)],
                            self._color, line_width)
        self._img_draw.line([(x_0 + 144, y_0 + 131), (x_0 + 124, y_0 + 111)],
                            self._color, line_width)

    def _draw_goodnight_text(self, data_w: WeatherBase, scale: 'ScaleType'):
        x_mid = self._display.WIDTH / 2
        y_mid = self._display.HEIGHT / 2
        # Message text
        message_str = "Good Night ^^"
        width, height = FONT_GL.getsize(message_str)
        message_x = x_mid - (width / 2)
        message_y = y_mid - (height / 2)
        self._img_draw.text((message_x, message_y), message_str, self._black, FONT_GL)
        # Weather text
        x_weather = 20
        y_weather = 210
        self._img_draw.text((x_weather, y_weather), data_w.get_temp_range(scale, 1),
                            self._color, FONT_GM)
        self._img_draw.text((x_weather, y_weather + 40), data_w.fetch_condition(1),
                            self._color, FONT_GS)

    def draw_date(self, x_pos: int, y_pos: int) -> None:
        """Draw date text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), strftime('%a %d %b %Y'), self._black,
                            FONT_L)

    def draw_time(self, x_pos: int, y_pos: int) -> None:
        """Draw time text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), strftime('%H:%M'), self._black, FONT_L)

    def draw_train_times(self, data_t: TrainBase, num_trains: int, x_pos: int,
                         y_pos: int) -> None:
        """Draw all train times text

        Each line: Train time, platform, destination station, ETA

        Args:
            data_t (TrainBase): TrainBase object
            num_trains (int): Number of train info to draw
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        for i in range(0, num_trains):
            self._img_draw.text((x_pos, y_pos + i * 30), data_t.fetch_train(i + 1),
                                self._black, FONT_S)

    def draw_weather_forecast(self, data_w: WeatherBase, scale: 'ScaleType', x_pos: int,
                              y_pos: int) -> None:
        """Draw all weather forecast text

        First line: current temperature and weather condition
        Second line: today's temperature range
        Third line: today's weather condition description
        Fourth line: tomorrow's weather condition description

        Args:
            data_w (WeatherBase): WeatherBase object
            scale (ScaleType): Celsius or Fahrenheit for formatting
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text((x_pos, y_pos), data_w.get_current_weather(scale),
                            self._black, FONT_L)
        self._img_draw.text((x_pos, y_pos + 45), data_w.get_temp_range(scale, 0),
                            self._black, FONT_M)
        self._img_draw.text((x_pos, y_pos + 75), data_w.fetch_condition(0), self._black,
                            FONT_M)
        self._img_draw.text((x_pos, y_pos + 105), data_w.fetch_condition(1),
                            self._black, FONT_S)

    def draw_weather_icon(self, icon: IconType, x_pos: int, y_pos: int) -> None:
        """Draws specified icon

        Args:
            icon (IconType): Weather IconType to draw
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        draw_icon_dispatcher: Dict[IconType, Callable] = {
            IconType.clear_sky: self.draw_sun_icon,
            IconType.few_clouds: self.draw_sun_cloud_icon,
            IconType.scattered_clouds: self.draw_cloud_icon,
            IconType.broken_clouds: self.draw_two_clouds_icon,
            IconType.shower_rain: self.draw_cloud_rain_icon,
            IconType.rain: self.draw_sun_cloud_rain_icon,
            IconType.thunderstorm: self.draw_cloud_lightning_icon,
            IconType.snow: self.draw_cloud_snow_icon,
            IconType.mist: self.draw_mist_icon,
        }
        draw_icon_dispatcher[icon](x_pos, y_pos)

    def draw_sun_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large sun icon

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_sun(x_pos + 7, y_pos)

    def draw_sun_cloud_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw small sun + large cloud icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_small_sun(x_pos, y_pos)
        self._gen_large_cloud(x_pos, y_pos + 5)

    def draw_cloud_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)

    def draw_two_clouds_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + small cloud icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_small_cloud(x_pos + 30, y_pos + 25)

    def draw_cloud_rain_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + two rain drop icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_raindrop(x_pos + 25, y_pos + 45)
        self._gen_raindrop(x_pos + 42, y_pos + 45)

    def draw_sun_cloud_rain_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw small sun, large cloud + two rain drop icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_small_sun(x_pos, y_pos)
        self._gen_large_cloud(x_pos, y_pos + 5)
        self._gen_raindrop(x_pos + 25, y_pos + 50)
        self._gen_raindrop(x_pos + 42, y_pos + 50)

    def draw_cloud_lightning_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + lightning bolt icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_lightning(x_pos + 30, y_pos + 45)

    def draw_cloud_snow_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw large cloud + snowflake icons

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_large_cloud(x_pos, y_pos)
        self._gen_snowflake(x_pos + 12, y_pos + 45)
        self._gen_snowflake(x_pos + 26, y_pos + 50)
        self._gen_snowflake(x_pos + 40, y_pos + 45)

    def draw_mist_icon(self, x_pos: int, y_pos: int) -> None:
        """Draw mist icon

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._gen_mist(x_pos + 5, y_pos)

    # =======================================================================
    # Private methods to draw icon sub-elements using ImageDraw primatives:
    # =======================================================================
    def _gen_large_sun(self, x_pos: int, y_pos: int) -> None:
        """Generate large sun icon
        """
        line_thickness: int = 5
        # Protruding rays
        self._img_draw.polygon((x_pos + 29, y_pos, x_pos + 34, y_pos + 16, x_pos + 24,
                                y_pos + 16, x_pos + 29, y_pos), self._black,
                               line_thickness)  # Top
        self._img_draw.polygon((x_pos + 29, y_pos + 56, x_pos + 34, y_pos + 46,
                                x_pos + 24, y_pos + 46, x_pos + 29, y_pos + 56),
                               self._black, line_thickness)  # Bottom
        self._img_draw.polygon((x_pos, y_pos + 28, x_pos + 17, y_pos + 23, x_pos + 17,
                                y_pos + 33, x_pos + 1, y_pos + 28), self._black,
                               line_thickness)  # Left
        self._img_draw.polygon((x_pos + 57, y_pos + 28, x_pos + 41, y_pos + 23,
                                x_pos + 41, y_pos + 33, x_pos + 57, y_pos + 28),
                               self._black, 5)  # Right
        self._img_draw.line((x_pos + 10, y_pos + 10, x_pos + 47, y_pos + 47),
                            self._black, line_thickness)
        self._img_draw.line((x_pos + 10, y_pos + 47, x_pos + 47, y_pos + 10),
                            self._black, line_thickness)
        # Sun circle
        self._img_draw.ellipse((x_pos + 12, y_pos + 12, x_pos + 45, y_pos + 45),
                               self._white)
        self._img_draw.ellipse((x_pos + 17, y_pos + 17, x_pos + 40, y_pos + 40),
                               self._black)

    def _gen_small_sun(self, x_pos: int, y_pos: int) -> None:
        """Generate small sun icon
        """
        line_thickness: int = 5
        # Protruding rays
        self._img_draw.line((x_pos + 5, y_pos + 5, x_pos + 25, y_pos + 25), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 5, y_pos + 25, x_pos + 25, y_pos + 5), self._black,
                            line_thickness)
        self._img_draw.polygon(
            (x_pos + 11, y_pos + 10, x_pos, y_pos + 15, x_pos + 20, y_pos + 19),
            self._black)
        self._img_draw.polygon(
            (x_pos + 15, y_pos, x_pos + 10, y_pos + 10, x_pos + 20, y_pos + 10),
            self._black)
        self._img_draw.polygon(
            (x_pos + 20, y_pos + 10, x_pos + 30, y_pos + 15, x_pos + 20, y_pos + 20),
            self._black)
        # Sun circle
        self._img_draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 25, y_pos + 25),
                               self._black)
        self._img_draw.ellipse((x_pos + 10, y_pos + 10, x_pos + 20, y_pos + 20),
                               self._white)

    def _gen_large_cloud(self, x_pos: int, y_pos: int) -> None:
        """Generate large cloud icon
        """
        # Outline
        self._img_draw.ellipse((x_pos, y_pos + 20, x_pos + 20, y_pos + 40), self._black)
        self._img_draw.ellipse((x_pos + 5, y_pos + 10, x_pos + 35, y_pos + 40),
                               self._black)
        self._img_draw.ellipse((x_pos + 15, y_pos, x_pos + 55, y_pos + 40), self._black)
        self._img_draw.ellipse((x_pos + 35, y_pos + 10, x_pos + 65, y_pos + 40),
                               self._black)
        # Negative Space
        self._img_draw.ellipse((x_pos + 5, y_pos + 25, x_pos + 15, y_pos + 35),
                               self._white)
        self._img_draw.ellipse((x_pos + 10, y_pos + 15, x_pos + 30, y_pos + 35),
                               self._white)
        self._img_draw.ellipse((x_pos + 20, y_pos + 5, x_pos + 50, y_pos + 35),
                               self._white)
        self._img_draw.ellipse((x_pos + 40, y_pos + 15, x_pos + 60, y_pos + 35),
                               self._white)

    def _gen_small_cloud(self, x_pos: int, y_pos: int) -> None:
        """Generate small cloud icon
        """
        # Outline
        self._img_draw.ellipse((x_pos, y_pos + 10, x_pos + 11, y_pos + 21), self._black)
        self._img_draw.ellipse((x_pos + 5, y_pos + 5, x_pos + 21, y_pos + 21),
                               self._black)
        self._img_draw.ellipse((x_pos + 10, y_pos, x_pos + 31, y_pos + 21), self._black)
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

    def _gen_lightning(self, x_pos: int, y_pos: int) -> None:
        """Generate lightning bolt icon
        """
        self._img_draw.polygon(
            ((x_pos, y_pos), (x_pos + 8, y_pos), (x_pos + 12, y_pos + 6),
             (x_pos + 6, y_pos + 6), (x_pos + 8, y_pos + 12), (x_pos, y_pos + 4),
             (x_pos + 7, y_pos + 4), (x_pos, y_pos)), self._black)

    def _gen_snowflake(self, x_pos: int, y_pos: int) -> None:
        """Generate snowflake icon
        """
        line_thickness: int = 2
        self._img_draw.line((x_pos + 5, y_pos, x_pos + 5, y_pos + 8), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 1, y_pos + 1, x_pos + 10, y_pos + 6), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 1, y_pos + 6, x_pos + 10, y_pos + 1), self._black,
                            line_thickness)

    def _gen_mist(self, x_pos: int, y_pos: int) -> None:
        """Generate mist icon
        """
        line_thickness: int = 4
        self._img_draw.line((x_pos + 22, y_pos, x_pos + 40, y_pos), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 4, y_pos + 8, x_pos + 47, y_pos + 8), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 15, y_pos + 16, x_pos + 60, y_pos + 16),
                            self._black, line_thickness)
        self._img_draw.line((x_pos, y_pos + 24, x_pos + 55, y_pos + 24), self._black,
                            line_thickness)
        self._img_draw.line((x_pos + 9, y_pos + 32, x_pos + 51, y_pos + 32),
                            self._black, line_thickness)
        self._img_draw.line((x_pos + 20, y_pos + 40, x_pos + 40, y_pos + 40),
                            self._black, line_thickness)
