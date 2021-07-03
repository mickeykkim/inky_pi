"""Base class for train model"""
from abc import ABC, abstractmethod
from typing import Dict


class TrainBase(ABC):
    """Abstract base class for all train models"""
    @abstractmethod
    def fetch_train(self, num: int) -> str:
        """Return requested train data"""
        ...


def abbreviate_stn_name(station_name: str) -> str:
    """Helper function to abbreviate station name by shortening words
    """
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
