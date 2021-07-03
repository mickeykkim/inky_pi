"""Inky_Pi train model module.

Fetches train data from Huxley2 (OpenLDBWS) and generates formatted data"""
import requests

from .train_base import TrainBase, abbreviate_stn_name  # type: ignore


class HuxleyOpenLDBWS(TrainBase):
    """Fetch and manage train data"""
    def __init__(self, stn_from: str, stn_to: str, num_trains: int) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

        Args:
            stn_from (str): From station
            stn_to (str): To station
            num_trains (int): Number of departing trains to request
        """
        response: requests.Response = requests.get(
            'https://huxley2.azurewebsites.net/departures/'
            f'{stn_from}/to/{stn_to}/{num_trains}')

        self._num: int = num_trains
        self._data: dict = response.json()

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
            raise ValueError(
                f"{num} is an invalid train request number (max: {self._num})")

        try:
            # Get all data
            platform: str = self._data['trainServices'][num -
                                                        1]['platform'][0:2]
            arrival_t: str = self._data['trainServices'][num - 1]['std']
            dest_stn: str = self._data['trainServices'][
                num - 1]['destination'][0]['locationName']
            dest_stn_abbr: str = abbreviate_stn_name(dest_stn)
            status: str = self._data['trainServices'][num - 1]['etd']
            return f'{arrival_t} | P{platform} to {dest_stn_abbr} - {status}'
        except (KeyError, TypeError, IndexError):
            try:
                # Try to get the error message & line wrap over each line
                line_length: int = 41
                return str(
                    self._data['nrccMessages'][0]['value'])[(num - 1) *
                                                            line_length:num *
                                                            line_length]
            except (KeyError, TypeError, IndexError):
                # Check if any trains are running
                if self._data['trainServices'] is None and num == 1:
                    dest: str = self._data['filterLocationName']
                    return f"No train services to {dest}."
                # Otherwise return generic message on line 1
                msg: str = "Error retrieving train data." if num == 1 else ""
                return f"{msg}"
