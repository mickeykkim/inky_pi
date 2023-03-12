"""Terminal drawing module.

Draws data to terminal"""
from time import strftime
from typing import Any, Dict, List, Tuple

from rich.console import Console

from inky_pi.configs import STATION_FROM, STATION_TO
from inky_pi.display.display_base import DisplayBase, DisplayObject
from inky_pi.train.train_base import TrainBase
from inky_pi.weather.weather_base import IconType, ScaleType, WeatherBase


class TerminalDraw(DisplayBase):
    """Draw text and weather emoji in terminal window"""

    todo = "[bold red]TODO[/bold red]"

    def __init__(self, base_color: str = "") -> None:
        """Initialise terminal text library

        Args:
            base_color: base color
        """
        if base_color:
            self.todo = f"[bold {base_color}]{self.todo}[/bold {base_color}]"
        self._console = Console()
        self._output: List[str] = []

    def render_text(self) -> None:
        """Render collected text onto the terminal"""
        self._console.print("\n".join(self._output))

    def draw_date(self, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Append date to terminal text

        Args:
            x_y: (x, y) coordinates
        """
        date = strftime("%a %d %b %Y")
        self._output.append(date)

    def draw_time(self, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Append time to terminal text

        Args:
            x_y: (x, y) coordinates
        """
        time = strftime("%H:%M")
        self._output.append(time)

    def draw_train_times(
        self, data_t: TrainBase, num_trains: int = 3, x_y: Tuple[int, int] = (0, 0)
    ) -> None:
        """Append train data to terminal text

        Args:
            data_t: train data
            num_trains: number of trains to display
            x_y: (x, y) coordinates
        """
        self._output.append(f"train schedule from {STATION_FROM} to {STATION_TO}:")
        for i in range(0, num_trains):
            train = data_t.fetch_train(i)
            self._output.append(train)

    def draw_weather_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
        disp_tomorrow: bool = False,
    ) -> None:
        """Append weather forecast to terminal text

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
            disp_tomorrow: display tomorrow's forecast
        """
        current_temp = data_w.get_current_temperature(scale)
        current_condition = data_w.get_current_condition()
        temp_range = data_w.get_temp_range(0, scale)
        condition = data_w.get_condition(0)
        self._output.append(f"now: {current_temp}")
        self._output.append(f"now: {current_condition}")
        self._output.append(f"today: {temp_range}")
        self._output.append(f"today: {condition}")
        if disp_tomorrow:
            tomorrow_condition = data_w.get_condition(1)
            self._output.append(f"tomorrow: {tomorrow_condition}")

    def draw_mini_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
        day: int = 0,
    ) -> None:
        """Append mini weather forecast to terminal text

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
            day: day to display
        """
        self._output.append(f"{self.todo}: draw_mini_forecast")

    def draw_weather_icon(self, icon: IconType, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Append weather icon to terminal text

        Args:
            icon: icon type
            x_y: (x, y) coordinates
        """
        draw_icon_dispatcher: Dict[IconType, str] = {
            IconType.CLEAR_SKY: "\U00002600",
            IconType.FEW_CLOUDS: "\U000026C5",
            IconType.SCATTERED_CLOUDS: "\U000026C5",
            IconType.BROKEN_CLOUDS: "\U00002601",
            IconType.SHOWER_RAIN: "\U0001F327",
            IconType.RAIN: "\U0001F326",
            IconType.THUNDERSTORM: "\U000026C8",
            IconType.SNOW: "\U0001F328",
            IconType.MIST: "\U0001F32B",
        }
        emoji = draw_icon_dispatcher[icon]
        self._output.append(emoji)

    def draw_forecast_icons(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
    ) -> None:
        """Append extended weather forecast icons to terminal text

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
        """
        self._output.append(f"{self.todo}: draw_forecast_icons")

    def draw_goodnight(
        self, data_w: WeatherBase, scale: ScaleType = ScaleType.CELSIUS
    ) -> None:
        """Append goodnight message to terminal text

        Args:
            data_w: weather data
            scale: scale type
        """
        message = "Good Night ^^"
        temp = data_w.get_temp_range(1, scale)
        self._output.append(message)
        self._output.append(temp)

    def __enter__(self) -> "TerminalDraw":
        """Enter context manager

        Returns:
            self
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager"""
        self.render_text()


def instantiate_terminal_display(display_object: DisplayObject) -> TerminalDraw:
    """Terminal display object creator

    Args:
        display_object (DisplayObject): display object containing model

    Returns:
        TerminalDraw: TerminalDraw object
    """
    return TerminalDraw(display_object.base_color)
