"""Terminal drawing module.

Draws data to terminal"""
from time import strftime
from typing import Any, Dict, List

from rich.console import Console

from inky_pi.display.display_base import DisplayBase
from inky_pi.train.train_base import TrainBase
from inky_pi.weather.weather_base import IconType, ScaleType, WeatherBase


class TerminalDraw(DisplayBase):
    """Draw text and shapes onto Inky e-ink display"""

    todo = "[bold red]TODO[/bold red]"

    def __init__(self, base_color: str = "") -> None:
        """Initialise display

        Args:
            base_color: base color
        """
        if base_color:
            self.todo = f"[bold {base_color}]{self.todo}[/bold {base_color}]"
        self._console = Console()
        self._output: List[str] = []

    def __enter__(self) -> "TerminalDraw":
        """Enter context manager

        Returns:
            self
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager"""
        self._console.print("\n".join(self._output))

    def draw_date(self, x_pos: int = 0, y_pos: int = 0) -> None:
        """Display date

        Args:
            x_pos: x position
            y_pos: y position
        """
        date = strftime("%a %d %b %Y")
        self._output.append(date)

    def draw_time(self, x_pos: int = 0, y_pos: int = 0) -> None:
        """Display time

        Args:
            x_pos: x position
            y_pos: y position
        """
        time = strftime("%H:%M")
        self._output.append(time)

    def draw_train_times(
        self, data_t: TrainBase, num_trains: int = 3, x_pos: int = 0, y_pos: int = 0
    ) -> None:
        """Display train data

        Args:
            data_t: train data
            num_trains: number of trains to display
            x_pos: x position
            y_pos: y position
        """
        for i in range(0, num_trains):
            train = data_t.fetch_train(i + 1)
            self._output.append(train)

    def draw_weather_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_pos: int = 0,
        y_pos: int = 0,
        disp_tomorrow: bool = False,
    ) -> None:
        """Display weather forecast

        Args:
            data_w: weather data
            scale: scale type
            x_pos: x position
            y_pos: y position
            disp_tomorrow: display tomorrow's forecast
        """
        current_temp = data_w.get_current_temperature(scale)
        self._output.append(current_temp)
        current_condition = data_w.get_current_condition()
        self._output.append(current_condition)
        temp_range = data_w.get_temp_range(0, scale)
        self._output.append(temp_range)
        condition = data_w.get_condition(0)
        self._output.append(condition)
        if disp_tomorrow:
            tomorrow_condition = data_w.get_condition(1)
            self._output.append(tomorrow_condition)

    def draw_mini_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_pos: int = 0,
        y_pos: int = 0,
        day: int = 0,
    ) -> None:
        """Display mini weather forecast

        Args:
            data_w: weather data
            scale: scale type
            x_pos: x position
            y_pos: y position
            day: day to display
        """
        self._output.append(f"{self.todo}: draw_mini_forecast")

    def draw_weather_icon(self, icon: IconType, x_pos: int = 0, y_pos: int = 0) -> None:
        """Display weather icon

        Args:
            icon: icon type
            x_pos: x position
            y_pos: y position
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
        x_pos: int = 0,
        y_pos: int = 0,
    ) -> None:
        """Display extended forecast icons

        Args:
            data_w: weather data
            scale: scale type
            x_pos: x position
            y_pos: y position
        """
        self._output.append(f"{self.todo}: draw_forecast_icons")

    def draw_goodnight(
        self, data_w: WeatherBase, scale: ScaleType = ScaleType.CELSIUS
    ) -> None:
        """Display goodnight message

        Args:
            data_w: weather data
            scale: scale type
        """
        message = "Good Night ^^"
        self._output.append(message)
        temp = data_w.get_temp_range(1, scale)
        self._output.append(temp)