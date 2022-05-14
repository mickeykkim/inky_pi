"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
import platform
from argparse import ArgumentParser, Namespace
from typing import Callable, Dict

# pylint: disable=wrong-import-position

if platform.machine() == "armv7l":
    from inky import InkyWHAT  # type: ignore

from loguru import logger

from inky_pi.configs import (
    EXCLUDE_FLAGS,
    LATITUDE,
    LONGITUDE,
    STATION_FROM,
    STATION_TO,
    TRAIN_API_TOKEN,
    TRAIN_MODEL,
    TRAIN_MODEL_URL,
    TRAIN_NUMBER,
    WEATHER_API_TOKEN,
    WEATHER_MODEL,
)
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.train.train_base import TrainBase
from inky_pi.util import (
    TrainModel,
    TrainObject,
    WeatherModel,
    WeatherObject,
    configure_logging,
    train_model_factory,
    weather_model_factory,
)
from inky_pi.weather.weather_base import ScaleType, WeatherBase

TRAIN_OBJECT = TrainObject(
    model=TrainModel[TRAIN_MODEL],
    station_from=STATION_FROM,
    station_to=STATION_TO,
    number=TRAIN_NUMBER,
    url=TRAIN_MODEL_URL,
    token=TRAIN_API_TOKEN,
)

WEATHER_OBJECT = WeatherObject(
    model=WeatherModel[WEATHER_MODEL],
    latitude=LATITUDE,
    longitude=LONGITUDE,
    exclude_flags=EXCLUDE_FLAGS,
    weather_api_token=WEATHER_API_TOKEN,
)


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    configure_logging()
    logger.debug("InkyPi initialized")

    # Send requests to API endpoints to set data
    train_data: TrainBase = train_model_factory(TRAIN_OBJECT)
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to inkyWHAT screen
    with InkyDraw(InkyWHAT("black")) as display:
        display.draw_date()
        display.draw_time()
        display.draw_train_times(train_data, TRAIN_NUMBER, 10, 50)
        display.draw_weather_forecast(weather_data, ScaleType.CELSIUS, 10, 150, True)
        display.draw_weather_icon(weather_data.get_icon(), 280, 200)


def weather() -> None:
    """inky_pi weather with extended forecast function

    Retrieves weather data from API endpoints, generates text and weather icon,
    and draws to inkyWHAT screen.
    """
    configure_logging()
    logger.debug("InkyPi initialized")

    # Send requests to API endpoints to set data
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to inkyWHAT screen
    with InkyDraw(InkyWHAT("black")) as display:
        display.draw_date()
        display.draw_time()
        display.draw_mini_forecast(weather_data)
        display.draw_weather_forecast(weather_data)
        display.draw_forecast_icons(weather_data)


def night() -> None:
    """inky_pi goodnight message main function"""
    configure_logging()
    logger.debug("InkyPi goodnight")

    # Send requests to API endpoints to set data
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    with InkyDraw(InkyWHAT("yellow")) as display:
        display.draw_goodnight(weather_data)


def terminal() -> None:
    """
    CLI for inky_pi.
    """
    print("TODO: terminal display option")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Inky_pi display function",
    )
    parser.add_argument(
        "--display", help="Display option (train, weather, night, terminal)"
    )
    args: Namespace = parser.parse_args()
    args_handler: Dict[str, Callable] = {
        "train": main,
        "weather": weather,
        "night": night,
        "terminal": terminal,
    }
    try:
        if args.display:
            args_handler[args.display]()
        else:
            main()
    except KeyError:
        logger.error("Invalid display option specified")
    except Exception as e:  # pylint: disable=broad-except # noqa: E722
        logger.exception(e)
