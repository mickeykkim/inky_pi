"""Inky_Pi train control module.

Fetches train data from huxley2 (OpenLDBWS) and generates formatted data"""
from typing import Dict

import requests


def req_train_data(stn_from: str, stn_to: str, num_trains: int) -> dict:
    """Requests train data from huxley2 (OpenLDBWS) train arrivals API endpoint

    Args:
        stn_from (str): From station
        stn_to (str): To station
        num_trains (int): Number of departing trains to request

    Returns:
        dict: Response OpenLDBWS JSON object as dictionary data
    """
    response = requests.get('https://huxley2.azurewebsites.net/departures/'
                            f'{stn_from}/to/{stn_to}/{num_trains}')
    return response.json()


def _abbreviate_station_name(station_name: str) -> str:
    """Abbreviate station name by shortening words like street, lane, etc.

    Args:
        station_name (str): Station name

    Returns:
        str: Abbreviated station name
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


def gen_next_train(data_t: dict, num: int) -> str:
    """Generate next train string

    String is returned in format:
        [hh:mm] to [Final Destination Station] - [Status]

    Args:
        data_t (dict): Dictionary data from OpenLDBWS train arrivals JSON req.
        num (int): Next train departing number

    Returns:
        str: Formatted string or error message
    """
    try:
        platform = data_t['trainServices'][num - 1]['platform']
        if platform == "None":
            platform = "?"
        train_arrival_t = data_t['trainServices'][num - 1]['std']
        dest_stn = data_t['trainServices'][num -
                                           1]['destination'][0]['locationName']
        abbr_dest_stn = _abbreviate_station_name(dest_stn)
        status = data_t['trainServices'][num - 1]['etd']
        return f'{train_arrival_t} (P{platform}) to {abbr_dest_stn} - {status}'
    except (KeyError, TypeError, IndexError):
        try:
            # Try to get the error message & line wrap over each line
            line_length = 41
            return str(data_t['nrccMessages'][0]['value'])[(num - 1) *
                                                           line_length:num *
                                                           line_length]
        except (KeyError, TypeError, IndexError):
            # If getting the error didn't work just return a generic message
            if num == 1:
                return "Error retrieving train data"
            return ""
