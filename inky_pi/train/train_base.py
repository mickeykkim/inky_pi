"""Base class and helper functions for train model"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional

from loguru import logger


def abbreviate_stn_name(station_name: str) -> str:
    """Helper function to abbreviate station name by shortening words

    Args:
        station_name (str): Station name

    Returns:
        str: Abbreviated station name
    """
    abbreviation_dict: Dict[str, str] = {
        "Station": "Stn",
        "Street": "St",
        "Lane": "Ln",
        "Court": "Ct",
        "Road": "Rd",
        "North": "N",
        "South": "S",
        "East": "E",
        "West": "W",
        "Thameslink": "TL",
    }
    for word, abbreviation in abbreviation_dict.items():
        station_name = station_name.replace(word, abbreviation)

    return station_name


class TrainModel(Enum):
    """Enum of train models"""

    HUXLEY2 = auto()
    OPEN_LIVE = auto()


@dataclass
class TrainObject:
    """Train object"""

    model: TrainModel
    station_from: str
    station_to: str
    number: int
    url: str = ""
    token: str = ""


class TrainBase(ABC):
    """Abstract base class for all train models"""

    def __init__(self):
        self._num: int = 0
        self._data: Optional[Any] = None
        self.origin: str = ""
        self.destination: str = ""

    @abstractmethod
    def retrieve_data(self, protocol: Any, train_object: TrainObject) -> None:
        """Retrieves train data from API; must be called after constructor

        Args:
            protocol: HTTP data protocol (e.g. requests or zeep)
            train_object: Train object
        """

    @abstractmethod
    def fetch_train(self, num: int) -> str:
        """Return requested train data

        Args:
            num (int): Desired train number

        Returns:
            str: Train data
        """

    @staticmethod
    def format_train_string(
        arrival_t: str, platform: str, dest_stn: str, status: str
    ) -> str:
        """Takes in a train's arrival time, platform, destination station, and status,
        and returns a string with the train's information in a display format.

        Args:
            arrival_t (str): The time the train is due to arrive at the station.
            platform (str): The platform number the train is arriving at.
            dest_stn (str): The destination station of the train.
            status (str): The status of the train.

        Returns:
            str: Formatted string
        """
        return (
            f"{arrival_t} | P{platform} to {abbreviate_stn_name(dest_stn)} - {status}"
        )

    # TODO: Change this to a generator implementation, update types, update tests
    @staticmethod
    def format_error_msg(error_msg: str, num: int) -> str:
        """Format error message by line wrapping over each line

        Args:
            error_msg (str): Error message
            num (int): Train number

        Returns:
            str: Formatted error message if num is 1 else empty string
        """
        line_length: int = 38
        if num == 0:
            logger.error(error_msg)
        return (error_msg[num * line_length : (num + 1) * line_length]).lstrip(" ")

    def _validate_number(self, num: int) -> None:
        """Check if train number is valid

        Args:
            num (int): Train number to check

        Raises:
            ValueError: Invalid train number
        """
        if num < 0 or num > self._num:
            raise ValueError(
                f"{num} is an invalid train request number (max: {self._num})"
            )
