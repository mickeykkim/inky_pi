"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional

from loguru import logger

from inky_pi.train.huxley2 import Huxley2  # type: ignore
from inky_pi.train.open_live import OpenLive  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore


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
    url: Optional[str] = None
    token: Optional[str] = None


def configure_logging() -> None:
    """See: https://loguru.readthedocs.io/en/stable/api.html"""
    logger.add("inky.log", rotation="5 MB", serialize=True)


def instantiate_huxley2(train_object: TrainObject) -> Huxley2:
    """Huxley2 does not require a url or api key"""
    return Huxley2(train_object.station_from, train_object.station_to,
                   train_object.number)


def instantiate_open_live(train_object: TrainObject) -> OpenLive:
    """Open Live requires a url and api key"""
    return OpenLive(train_object.station_from, train_object.station_to,
                    train_object.number, train_object.url, train_object.token)


def train_model_factory(train_object: TrainObject) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        train_object (TrainObject): train object containing train model
    """
    if train_object.model == TrainModel.OPEN_LIVE and (train_object.url is None
                                                       or train_object.token is None):
        raise ValueError('Open Live requires URL and API token.')

    train_handler: Dict[TrainModel, TrainBase] = {
        TrainModel.OPEN_LIVE: instantiate_open_live,
        TrainModel.HUXLEY2: instantiate_huxley2,
    }
    return train_handler[train_object.model](train_object)
