"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from typing import Dict

from inky import InkyWHAT  # type: ignore

from inky_pi.configs import (EXCLUDE_FLAGS, LATITUDE, LONGITUDE, STATION_FROM,
                             STATION_TO, TRAIN_API_TOKEN, TRAIN_MODEL,
                             TRAIN_MODEL_URL, TRAIN_NUMBER, WEATHER_API_TOKEN)
from inky_pi.display.inky_draw import InkyDraw  # type: ignore
from inky_pi.train.huxley2 import Huxley2  # type: ignore
from inky_pi.train.open_live import OpenLive  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore
from inky_pi.weather.open_weather_map import OpenWeatherMap  # type: ignore
from inky_pi.weather.weather_base import ScaleType, WeatherBase  # type: ignore


# pylint: disable=unused-argument
def _instantiate_huxley2(station_from: str, station_to: str, number: int,
                         *args) -> Huxley2:
    """Huxley2 does not require a url or api key"""
    return Huxley2(station_from, station_to, number)


def _instantiate_open_live(station_from: str, station_to: str, number: int, url: str,
                           token: str) -> OpenLive:
    return OpenLive(station_from, station_to, number, url, token)


def _train_model_factory(model: str,
                         station_from: str,
                         station_to: str,
                         number: int,
                         url: str = None,
                         token: str = None) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        model (str): Train model name, "huxley2" or "open_live"
        station_from (str): Departure station
        station_to (str): Destination station
        number (int): Number of departing trains to retrieve
        url (str): [Optional] Open Live URL
        token (str): [Optional] Open Live API token
    """
    if model == "open_live" and (url is None or token is None):
        raise ValueError('Open Live requires URL and API token.')

    train_dict: Dict[str, TrainBase] = {
        "open_live": _instantiate_open_live,
        "huxley2": _instantiate_huxley2,
    }
    return train_dict[model](station_from, station_to, number, url, token)


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set data
    train_data: TrainBase = _train_model_factory(TRAIN_MODEL, STATION_FROM, STATION_TO,
                                                 TRAIN_NUMBER, TRAIN_MODEL_URL,
                                                 TRAIN_API_TOKEN)

    weather_data: WeatherBase = OpenWeatherMap(LATITUDE, LONGITUDE, EXCLUDE_FLAGS,
                                               WEATHER_API_TOKEN)

    # Set the display object configured with specified Inky display model
    display = InkyDraw(InkyWHAT('black'))

    # Draw text and weather icon on display object at specified x, y coords
    display.draw_date(10, 10)
    display.draw_time(297, 10)
    display.draw_train_times(train_data, TRAIN_NUMBER, 10, 60)
    display.draw_weather_forecast(weather_data, ScaleType.celsius, 10, 160)
    display.draw_weather_icon(weather_data.get_icon(), 300, 200)

    # Render display object on Inky display screen
    display.render_screen()


if __name__ == "__main__":
    main()
