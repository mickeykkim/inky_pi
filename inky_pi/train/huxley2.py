"""Inky_Pi train model module.

Fetches train data from Huxley2 (OpenLDBWS) and generates formatted data"""
from typing import Any, Dict

import requests
from loguru import logger

from inky_pi.train.train_base import TrainBase, TrainObject, abbreviate_stn_name


class Huxley2(TrainBase):
    """Fetch and manage train data"""

    def __init__(self) -> None:
        self._num: int = 0
        self._data: dict = {}
        self._origin: str = ""
        self._destination: str = ""

    def retrieve_data(self, protocol: Any, train_object: TrainObject) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

        More info here: https://huxley2.azurewebsites.net/

        Args:
            protocol (Any): Requests object for HTTP requests
            train_object (TrainObject): Train object
        """
        response: Any = protocol.get(
            "https://huxley2.azurewebsites.net/departures/"
            f"{train_object.station_from}/to/"
            f"{train_object.station_to}/{train_object.number}"
        )

        self._num = train_object.number
        try:
            self._data = response.json()
            self._origin = abbreviate_stn_name(self._data["locationName"])
            self._destination = abbreviate_stn_name(self._data["filterLocationName"])
        except protocol.exceptions.JSONDecodeError as exc:
            logger.error("Error retrieving train data (check stations?).")
            raise ValueError(f"Invalid train data request: {train_object}") from exc

    def fetch_train(self, num: int) -> str:
        """Generate next train string

        String is returned in format:
            [hh:mm] | [Platform #] to [Final Destination Station] - [Status]

        Args:
            num (int): Next train departing number

        Returns:
            str: Formatted string or error message
        """
        if num < 0 or num > self._num:
            logger.error("Invalid fetch_train num", num)
            raise ValueError(
                f"{num} is an invalid train request number (max: {self._num})"
            )

        try:
            # Get all data
            service: Dict = self._data["trainServices"][num - 1]
            platform: str = service["platform"][0:2]
            arrival_t: str = service["std"]
            dest_stn: str = service["destination"][0]["locationName"]
            dest_stn_abbr: str = abbreviate_stn_name(dest_stn)
            status: str = service["etd"]
            return f"{arrival_t} | P{platform} to {dest_stn_abbr} - {status}"
        except (KeyError, TypeError, IndexError):
            # Try to get the error message & line wrap over each line
            l_len: int = 38
            try:
                error_msg = str(self._data["nrccMessages"][0]["value"])
                if num == 1:
                    logger.warning(error_msg)
                return (error_msg[(num - 1) * l_len : num * l_len]).lstrip(" ")
            except (KeyError, TypeError, IndexError) as exc:
                logger.error("Could not get train error message", repr(exc))
                # Check if any trains are running
                error_msg = f"No trains to {self._destination} from {self._origin}."
                if num == 1:
                    logger.warning(error_msg)
                if self._data["trainServices"] is None:
                    return (error_msg[(num - 1) * l_len : num * l_len]).lstrip(" ")
                # Otherwise, return generic message on line 1
                msg: str = "Error retrieving train data." if num == 1 else ""
                return f"{msg}"


def instantiate_huxley2(train_object: TrainObject) -> Huxley2:
    """Huxley2 object creator

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        Huxley2: Huxley2 object
    """
    train_base = Huxley2()
    train_base.retrieve_data(requests, train_object)
    return train_base
