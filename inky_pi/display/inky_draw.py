"""Inky_Pi drawing module.

Draw strings and icons"""
import platform
from datetime import datetime, timedelta
from time import strftime
from typing import Any, Callable, Dict, Tuple

# pylint: disable=no-name-in-module
from font_fredoka_one import FredokaOne  # type: ignore
from font_hanken_grotesk import HankenGroteskBold  # type: ignore

# pylint: enable=no-name-in-module
from PIL import Image, ImageDraw, ImageFont  # type: ignore

from inky_pi.display.display_base import DisplayBase, DisplayModel, DisplayObject
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

    def __init__(self, display_driver: Any) -> None:
        """Create display and image drawing objects
        inky_model can be an InkyWHAT model or a DesktopDisplayDriver object

        Args:
            display_driver (Any): Display driver (InkyWHAT or DesktopDisplayDriver)
        """
        self._display: Any = display_driver
        self._img: Image = Image.new(
            "P", (self._display.WIDTH, self._display.HEIGHT), color="white"
        )
        self._img_draw: ImageDraw = ImageDraw.Draw(self._img)
        self._black: Any = self._display.BLACK
        self._white: Any = self._display.WHITE
        self._color: Any = self._display.YELLOW

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
        x_mid, y_mid = self._display.WIDTH / 2, self._display.HEIGHT / 2
        gen_closed_eye_icon(self._img_draw, self._color, (x_mid, y_mid))
        # Message text
        message_str = "Good Night ^^"
        width, height = FONT_GL.getsize(message_str)
        message_x, message_y = x_mid - (width / 2), y_mid - (height / 2)
        self._img_draw.text((message_x, message_y), message_str, self._black, FONT_GL)
        # Weather text
        x_weather, y_weather = 20, 210
        self._img_draw.text(
            (x_weather, y_weather),
            data_w.get_temp_range(1, scale),
            self._color,
            FONT_GM,
        )
        self._img_draw.text(
            (x_weather, y_weather + 40), data_w.get_condition(1), self._color, FONT_GS
        )

    def draw_date(self, x_y: Tuple[int, int] = (10, 5)) -> None:
        """Draw date text

        Args:
            x_y: (x, y) coordinates
        """
        self._img_draw.text(x_y, strftime("%a %d %b %Y"), self._black, FONT_S)

    def draw_time(self, x_y: Tuple[int, int] = (257, 5)) -> None:
        """Draw time text

        Args:
            x_y: (x, y) coordinates
        """
        self._img_draw.text(x_y, f"Updated {strftime('%H:%M')}", self._black, FONT_S)

    def draw_train_times(
        self, data_t: TrainBase, num_trains: int = 3, x_y: Tuple[int, int] = (10, 205)
    ) -> None:
        """Draw all train times text

        Each line: Train time, platform, destination station, ETA

        Args:
            data_t (TrainBase): TrainBase object
            num_trains (int): Number of train info to draw
            x_y: (x, y) coordinates
        """
        for i in range(0, num_trains):
            self._img_draw.text(
                (x_y[0], x_y[1] + i * 30),
                data_t.fetch_train(i),
                self._black,
                FONT_S,
            )

    def draw_weather_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (135, 50),
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
            x_y: (x, y) coordinates
            disp_tomorrow (bool): Display tomorrow's weather forecast
        """
        self._img_draw.text(
            x_y,
            data_w.get_current_temperature(scale),
            self._black,
            FONT_XL,
        )
        self._img_draw.text(
            (x_y[0] + 140, x_y[1] + 13),
            data_w.get_current_condition(),
            self._black,
            FONT_M,
        )
        self._img_draw.text(
            (x_y[0], x_y[1] + 50),
            data_w.get_temp_range(0, scale),
            self._black,
            FONT_M,
        )
        self._img_draw.text(
            (x_y[0], x_y[1] + 80), data_w.get_condition(0), self._black, FONT_M
        )
        if disp_tomorrow:
            self._img_draw.text(
                (x_y[0], x_y[1] + 110),
                "tomorrow: " + data_w.get_condition(1),
                self._black,
                FONT_S,
            )

    def draw_weather_icon(
        self,
        icon: IconType,
        x_y: Tuple[int, int] = (30, 90),
    ) -> None:
        """Draws specified icon

        Args:
            icon (IconType): Weather IconType to draw
            x_y: (x, y) coordinates
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
        draw_icon_dispatcher[icon](self._img_draw, self._black, self._white, x_y)

    def draw_mini_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (30, 40),
        day: int = 0,
    ) -> None:
        """Draws weather forecast icons and text future day

        Args:
            data_w (WeatherBase): WeatherBase object
            scale (ScaleType): Celsius or Fahrenheit for formatting
            x_y: (x, y) coordinates
            day (int): Day to display
        """
        new_date = datetime.now() + timedelta(days=day)
        if day > 0:
            self._img_draw.text(
                (x_y[0] + 10, x_y[1] + 5),
                new_date.strftime("%a %d"),
                self._black,
                FONT_XS,
            )
        self.draw_weather_icon(data_w.get_icon(day), (x_y[0], x_y[1] + 27))
        self._img_draw.text(
            ((x_y[0] + 10 if day > 0 else x_y[0]), x_y[1] + 90),
            data_w.get_future_weather(day, scale),
            self._black,
            FONT_XS if day > 0 else FONT_S,
        )

    def draw_forecast_icons(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (10, 180),
    ) -> None:
        """Draws weather forecast icons and text for next 5 days

        Args:
            data_w (WeatherBase): WeatherBase object
            scale (ScaleType): Celsius or Fahrenheit for formatting
            x_y: (x, y) coordinates
        """
        spacing: int = 78
        for i in range(0, 5):
            self.draw_mini_forecast(
                data_w, scale, (x_y[0] + (i * spacing), x_y[1]), i + 1
            )

    def __enter__(self) -> "InkyDraw":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager; render the drawn screen"""
        self.render_screen()


def _import_inky_what() -> Any:
    """This is a wrapper that imports InkyWHAT to allow mocking it in tests.

    Returns:
        InkyWHAT: Raspberry pi InkyWHAT library
    """
    if platform.machine() == "armv7l":
        # pylint: disable=import-outside-toplevel
        from inky import (  # type: ignore # noqa: E0401 # pylint: disable=import-error
            InkyWHAT,
        )

        return InkyWHAT
    raise ImportError("InkyWHAT library unavailable (are you on a Raspberry Pi?)")


def instantiate_inky_display(display_object: DisplayObject) -> InkyDraw:
    """Inky display object creator

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        InkyDraw: InkyDraw object
    """
    display_driver = (
        _import_inky_what()
        if display_object.model == DisplayModel.INKY_WHAT
        else DesktopDisplayDriver
    )
    return InkyDraw(display_driver(f"{display_object.base_color}"))
