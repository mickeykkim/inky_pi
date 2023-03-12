"""Inky_Pi train model module.

Fetches train data from Huxley2 (OpenLDBWS) and generates formatted data"""
from typing import Any, Dict

import requests
from loguru import logger

from inky_pi.train.train_base import TrainBase, TrainObject, abbreviate_stn_name


class Huxley2(TrainBase):
    """Fetch and manage train data"""

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
            self.origin = abbreviate_stn_name(self._data["locationName"])
            self.destination = abbreviate_stn_name(self._data["filterLocationName"])
        except protocol.exceptions.JSONDecodeError as exc:
            logger.error("Error retrieving train data (check stations?).")
            raise ValueError(f"Invalid train data request: {train_object}") from exc

    def _handle_error(self, num: int) -> str:
        """Log error and raise exception

        Args:
            num (int): Train number

        Raises:
            Exception: Exception to raise
        """
        if not self._data:
            raise ValueError("No train data available.")

        try:
            error_msg = str(self._data["nrccMessages"][0]["value"])
            return TrainBase.format_error_msg(error_msg, num)
        except (AttributeError, TypeError, KeyError, IndexError):
            error_msg = f"No trains to {self.destination} from {self.origin}."
            return TrainBase.format_error_msg(error_msg, num)

    def fetch_train(self, num: int) -> str:
        """Generate next train string

        String is returned in format:
            [hh:mm] | [Platform #] to [Final Destination Station] - [Status]

        Args:
            num (int): Next train departing number starting from 0

        Returns:
            str: Formatted string or error message
        """
        self._validate_number(num)
        if not self._data:
            raise ValueError("No train data available.")

        try:
            service: Dict = self._data["trainServices"][num]
            platform: str = service["platform"][0:2]
            arrival_t: str = service["std"]
            dest_stn: str = service["destination"][0]["locationName"]
            status: str = service["etd"]
            return TrainBase.format_train_string(arrival_t, platform, dest_stn, status)
        except (KeyError, TypeError, IndexError):
            return self._handle_error(num)


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
