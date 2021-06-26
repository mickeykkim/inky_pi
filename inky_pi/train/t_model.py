"""Inky_Pi train model module.

Fetches train data from OpenLDBWS and generates formatted data"""
from typing import Dict

import requests


class TrainModel:
    """Fetch and manage train data"""
    def __init__(self, stn_from: str, stn_to: str, num_trains: int) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

        Args:
            stn_from (str): From station
            stn_to (str): To station
            num_trains (int): Number of departing trains to request
        """
        response = requests.get('https://huxley2.azurewebsites.net/departures/'
                                f'{stn_from}/to/{stn_to}/{num_trains}')

        self._num = num_trains
        self._data = response.json()

    def fetch_train(self, num: int) -> str:
        """Generate next train string

        String is returned in format:
            [hh:mm] (Platform #) to [Final Destination Station] - [Status/ETD]

        Args:
            num (int): Next train departing number

        Returns:
            str: Formatted string or error message
        """
        if num > self._num:
            raise ValueError(
                f"{num} is greater than maximum train number {self._num}")

        try:
            # Get all data
            platform = self._data['trainServices'][num - 1]['platform']
            if platform == "None":
                platform = "?"
            arrival_t = self._data['trainServices'][num - 1]['std']
            dest_stn = self._data['trainServices'][
                num - 1]['destination'][0]['locationName']
            dest_stn_abbr = self._abbreviate_stn_name(dest_stn)
            status = self._data['trainServices'][num - 1]['etd']
            return f'{arrival_t} (P{platform}) to {dest_stn_abbr} - {status}'
        except (KeyError, TypeError, IndexError):
            try:
                # Try to get the error message & line wrap over each line
                line_length = 41
                return str(
                    self._data['nrccMessages'][0]['value'])[(num - 1) *
                                                            line_length:num *
                                                            line_length]
            except (KeyError, TypeError, IndexError):
                # If getting the error didn't work just return generic message
                if num == 1:
                    return "Error retrieving train data"
                return ""

    def _abbreviate_stn_name(self, station_name: str) -> str:
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
        for key, value in abbreviation_dict.items():
            station_name = station_name.replace(key, value)

        return station_name
