"""Base class and helper functions for train model"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict


def abbreviate_stn_name(station_name: str) -> str:
    """Helper function to abbreviate station name by shortening words"""
    abbreviation_dict: Dict[str, str] = {
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
