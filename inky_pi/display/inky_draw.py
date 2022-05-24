"""Inky_Pi drawing module.

Draw strings and icons"""
from datetime import datetime, timedelta
from time import strftime
from typing import Any, Callable, Dict

# pylint: disable=no-name-in-module
from font_fredoka_one import FredokaOne  # type: ignore
from font_hanken_grotesk import HankenGroteskBold  # type: ignore

# pylint: enable=no-name-in-module
from PIL import Image, ImageDraw, ImageFont  # type: ignore

from inky_pi.display.display_base import DisplayBase
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
from inky_pi.train.train_base import TrainBase
from inky_pi.weather.weather_base import IconType, ScaleType, WeatherBase

# Font constants
FONT_XS = ImageFont.truetype(HankenGroteskBold, 16)
FONT_S = ImageFont.truetype(HankenGroteskBold, 20)
FONT_M = ImageFont.truetype(HankenGroteskBold, 25)
FONT_L = ImageFont.truetype(HankenGroteskBold, 35)
FONT_XL = ImageFont.truetype(HankenGroteskBold, 40)
FONT_GS = ImageFont.truetype(FredokaOne, 25)
FONT_GM = ImageFont.truetype(FredokaOne, 30)
FONT_GL = ImageFont.truetype(FredokaOne, 40)


class InkyDraw(DisplayBase):
    """Draw text and shapes onto Inky e-ink display"""

    def __init__(self, inky_model: Any) -> None:
        """Create display and image drawing objects
        inky_model can be an InkyWHAT model or a DesktopDisplayDriver object

        Args:
            inky_model (Any): Inky display model (i.e. InkyWHAT('black'))
        """
        self._display: Any = inky_model
        self._img: Image = Image.new(
            "P", (self._display.WIDTH, self._display.HEIGHT), color="white"
        )
        self._img_draw: ImageDraw = ImageDraw.Draw(self._img)
        self._black: Any = self._display.BLACK
        self._white: Any = self._display.WHITE
        self._color: Any = self._display.YELLOW

    def __enter__(self) -> "InkyDraw":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager; render the drawn screen"""
        self.render_screen()

    def render_screen(self) -> None:
        """Render border, images (w/text) on inky screen and show on display"""
        self._display.set_image(self._img)
        self._display.set_border(self._black)
        self._display.show()

    def draw_goodnight(
        self, data_w: WeatherBase, scale: ScaleType = ScaleType.CELSIUS
    ) -> None:
        """Render goodnight screen

        Args:
            data_w (WeatherBase): Weather data object
            scale (ScaleType): Scale type
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
        self._img_draw.arc(
            [(x_0, y_0), (x_1, y_1)], a_start, a_end, self._color, line_width
        )
        self._img_draw.line(
            [(x_0 + 9, y_0 + 131), (x_0 + 29, y_0 + 111)], self._color, line_width
        )
        self._img_draw.line(
            [(x_0 + 49, y_0 + 147), (x_0 + 59, y_0 + 122)], self._color, line_width
        )
        self._img_draw.line(
            [(x_0 + 104, y_0 + 147), (x_0 + 94, y_0 + 122)], self._color, line_width
        )
        self._img_draw.line(
            [(x_0 + 144, y_0 + 131), (x_0 + 124, y_0 + 111)], self._color, line_width
        )

    def _draw_goodnight_text(
        self, data_w: WeatherBase, scale: ScaleType = ScaleType.CELSIUS
    ):
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
        self._img_draw.text(
            (x_weather, y_weather),
            data_w.get_temp_range(1, scale),
            self._color,
            FONT_GM,
        )
        self._img_draw.text(
            (x_weather, y_weather + 40), data_w.get_condition(1), self._color, FONT_GS
        )

    def draw_date(self, x_pos: int = 10, y_pos: int = 5) -> None:
        """Draw date text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text(
            (x_pos, y_pos), strftime("%a %d %b %Y"), self._black, FONT_S
        )

    def draw_time(self, x_pos: int = 257, y_pos: int = 5) -> None:
        """Draw time text

        Args:
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        self._img_draw.text(
            (x_pos, y_pos), f"Updated {strftime('%H:%M')}", self._black, FONT_S
        )

    def draw_train_times(
        self, data_t: TrainBase, num_trains: int = 3, x_pos: int = 10, y_pos: int = 205
    ) -> None:
        """Draw all train times text

        Each line: Train time, platform, destination station, ETA

        Args:
            data_t (TrainBase): TrainBase object
            num_trains (int): Number of train info to draw
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        for i in range(0, num_trains):
            self._img_draw.text(
                (x_pos, y_pos + i * 30), data_t.fetch_train(i + 1), self._black, FONT_S
            )

    def draw_weather_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_pos: int = 135,
        y_pos: int = 50,
        disp_tomorrow: bool = False,
    ) -> None:
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
            disp_tomorrow (bool): Display tomorrow's weather forecast
        """
        self._img_draw.text(
            (x_pos, y_pos),
            data_w.get_current_temperature(scale),
            self._black,
            FONT_XL,
        )
        self._img_draw.text(
            (x_pos + 140, y_pos + 13),
            data_w.get_current_condition(),
            self._black,
            FONT_M,
        )
        self._img_draw.text(
            (x_pos, y_pos + 50),
            data_w.get_temp_range(0, scale),
            self._black,
            FONT_M,
        )
        self._img_draw.text(
            (x_pos, y_pos + 80), data_w.get_condition(0), self._black, FONT_M
        )
        if disp_tomorrow:
            self._img_draw.text(
                (x_pos, y_pos + 110),
                "tomorrow: " + data_w.get_condition(1),
                self._black,
                FONT_S,
            )

    def draw_weather_icon(
        self,
        icon: IconType,
        x_pos: int = 30,
        y_pos: int = 90,
    ) -> None:
        """Draws specified icon

        Args:
            icon (IconType): Weather IconType to draw
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        draw_icon_dispatcher: Dict[IconType, Callable] = {
            IconType.CLEAR_SKY: draw_sun_icon,
            IconType.FEW_CLOUDS: draw_sun_cloud_icon,
            IconType.SCATTERED_CLOUDS: draw_cloud_icon,
            IconType.BROKEN_CLOUDS: draw_two_clouds_icon,
            IconType.SHOWER_RAIN: draw_cloud_rain_icon,
            IconType.RAIN: draw_sun_cloud_rain_icon,
            IconType.THUNDERSTORM: draw_cloud_lightning_icon,
            IconType.SNOW: draw_cloud_snow_icon,
            IconType.MIST: draw_mist_icon,
        }
        draw_icon_dispatcher[icon](
            self._img_draw, self._black, self._white, x_pos, y_pos
        )

    def draw_mini_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_pos: int = 30,
        y_pos: int = 40,
        day: int = 0,
    ) -> None:
        """Draws weather forecast icons and text future day

        Args:
            data_w (WeatherBase): WeatherBase object
            scale (ScaleType): Celsius or Fahrenheit for formatting
            x_pos (int): X position offset
            y_pos (int): Y position offset
            day (int): Day to display
        """
        new_date = datetime.now() + timedelta(days=day)
        if day > 0:
            self._img_draw.text(
                (x_pos + 10, y_pos + 5),
                new_date.strftime("%a %d"),
                self._black,
                FONT_XS,
            )
        self.draw_weather_icon(data_w.get_icon(day), x_pos, y_pos + 27)
        self._img_draw.text(
            ((x_pos + 10 if day > 0 else x_pos), y_pos + 90),
            data_w.get_future_weather(day, scale),
            self._black,
            FONT_XS if day > 0 else FONT_S,
        )

    def draw_forecast_icons(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_pos: int = 10,
        y_pos: int = 180,
    ) -> None:
        """Draws weather forecast icons and text for next 5 days

        Args:
            data_w (WeatherBase): WeatherBase object
            scale (ScaleType): Celsius or Fahrenheit for formatting
            x_pos (int): X position offset
            y_pos (int): Y position offset
        """
        for i in range(0, 5):
            self.draw_mini_forecast(data_w, scale, x_pos + (i * 78), y_pos, i + 1)
