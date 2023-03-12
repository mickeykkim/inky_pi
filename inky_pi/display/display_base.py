"""Inky Pi base display module.

Abstract class for all display models"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Tuple

from inky_pi.train.train_base import TrainBase
from inky_pi.weather.weather_base import IconType, ScaleType, WeatherBase


class DisplayModel(Enum):
    """Enum of display models"""

    INKY_WHAT = auto()
    TERMINAL = auto()
    DESKTOP = auto()


@dataclass
class DisplayObject:
    """Display object"""

    model: DisplayModel
    base_color: str = ""


class DisplayBase(ABC):
    """Abstract base class for all display models"""

    @abstractmethod
    def draw_date(self, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Display date

        Args:
            x_y: (x, y) coordinates
        """

    @abstractmethod
    def draw_time(self, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Display time

        Args:
            x_y: (x, y) coordinates
        """

    @abstractmethod
    def draw_train_times(
        self, data_t: TrainBase, num_trains: int = 0, x_y: Tuple[int, int] = (0, 0)
    ) -> None:
        """Display train data

        Args:
            data_t: train data
            num_trains: number of trains to display
            x_y: (x, y) coordinates
        """

    @abstractmethod
    def draw_weather_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
        disp_tomorrow: bool = False,
    ) -> None:
        """Display weather forecast

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
            disp_tomorrow: display tomorrow's forecast
        """

    @abstractmethod
    def draw_mini_forecast(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
        day: int = 0,
    ) -> None:
        """Display mini weather forecast

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
            day: day to display
        """

    @abstractmethod
    def draw_weather_icon(self, icon: IconType, x_y: Tuple[int, int] = (0, 0)) -> None:
        """Display weather icon

        Args:
            icon: icon type
            x_y: (x, y) coordinates
        """

    @abstractmethod
    def draw_forecast_icons(
        self,
        data_w: WeatherBase,
        scale: ScaleType = ScaleType.CELSIUS,
        x_y: Tuple[int, int] = (0, 0),
    ) -> None:
        """Display extended forecast icons

        Args:
            data_w: weather data
            scale: scale type
            x_y: (x, y) coordinates
        """

    @abstractmethod
    def draw_goodnight(
        self, data_w: WeatherBase, scale: ScaleType = ScaleType.CELSIUS
    ) -> None:
        """Display goodnight message

        Args:
            data_w: weather data
            scale: scale type
        """

    @abstractmethod
    def __enter__(self) -> "DisplayBase":
        """Enter context manager

        Returns:
            self
        """

    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager"""
