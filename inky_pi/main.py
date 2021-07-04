"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from typing import Dict

from inky import InkyWHAT  # type: ignore

from inky_pi.configs import (T_LDB_TOKEN, T_MODEL, T_NUM, T_STATION_FROM,
                             T_STATION_TO, T_WSDL, W_API_KEY, W_EXCLUDE,
                             W_LATITUDE, W_LONGITUDE)
from inky_pi.display.inky_draw import InkyDraw  # type: ignore
from inky_pi.train.huxley2_openldbws import HuxleyOpenLDBWS  # type: ignore
from inky_pi.train.openldbws import OpenLDBWS  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore
from inky_pi.weather.openweathermap import OpenWeatherMap  # type: ignore
from inky_pi.weather.weather_base import ScaleType, WeatherBase  # type: ignore


# pylint: disable=unused-argument
def _instantiate_huxley2(t_station_from: str, t_station_to: str, t_num: int,
                         *args) -> HuxleyOpenLDBWS:
    return HuxleyOpenLDBWS(t_station_from, t_station_to, t_num)


def _instantiate_openldbws(t_station_from: str, t_station_to: str, t_num: int,
                           t_wsdl: str, t_ldb_token: str) -> OpenLDBWS:
    return OpenLDBWS(t_station_from, t_station_to, t_num, t_wsdl, t_ldb_token)


def _train_model_factory(t_model: str,
                         t_station_from: str,
                         t_station_to: str,
                         t_num: int,
                         t_wsdl: str = None,
                         t_ldb_token: str = None) -> TrainBase:
    """Selects and instantiates the defined train model to use

    Args:
        t_model (str): Train model name, "huxley2" or "openldbws"
        t_station_from (str): Departure station
        t_station_to (str): Destination station
        t_num (int): Number of departing trains to retrieve
        t_wdls (str): [Optional] OpenLDBWS WSDL URL
        t_ldb_token (str): [Optional] OpenLDBWS API token
    """
    if t_model == "openldbws" and (t_wsdl is None or t_ldb_token is None):
        raise ValueError('OpenLDBWS requires WSDL and LDB token.')

    train_dict: Dict[str, TrainBase] = {
        "openldbws": _instantiate_openldbws,
        "huxley2": _instantiate_huxley2,
    }
    return train_dict[t_model](t_station_from, t_station_to, t_num, t_wsdl,
                               t_ldb_token)


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set data
    train_data: TrainBase = _train_model_factory(T_MODEL, T_STATION_FROM,
                                                 T_STATION_TO, T_NUM, T_WSDL,
                                                 T_LDB_TOKEN)

    weather_data: WeatherBase = OpenWeatherMap(W_LATITUDE, W_LONGITUDE,
                                               W_EXCLUDE, W_API_KEY)

    # Set the display object configured with specified Inky display model
    display = InkyDraw(InkyWHAT('black'))

    # Draw text and weather icon on display object at specified x, y coords
    display.draw_date(10, 10)
    display.draw_time(297, 10)
    display.draw_train_times(train_data, T_NUM, 10, 60)
    display.draw_weather_forecast(weather_data, ScaleType.celsius, 10, 160)
    display.draw_weather_icon(weather_data.get_icon(), 300, 200)

    # Render display object on Inky display screen
    display.render_screen()


if __name__ == "__main__":
    main()
