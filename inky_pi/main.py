"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from argparse import ArgumentParser, Namespace
from typing import Callable, Dict

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
from inky_pi.display.display_base import DisplayBase
from inky_pi.train.train_base import TrainBase
from inky_pi.util import (
    DisplayModel,
    DisplayObject,
    TrainModel,
    TrainObject,
    WeatherModel,
    WeatherObject,
    configure_logging,
    display_model_factory,
    import_display,
    train_model_factory,
    weather_model_factory,
)
from inky_pi.weather.weather_base import ScaleType, WeatherBase

# Define objects to be used in fetching and displaying data
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

DEFAULT_DISPLAY_OBJECT = DisplayObject(
    model=DisplayModel.INKY_WHAT,
    base_color="black",
)

NIGHT_DISPLAY_OBJECT = DisplayObject(
    model=DisplayModel.INKY_WHAT,
    base_color="yellow",
)


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set data
    train_data: TrainBase = train_model_factory(TRAIN_OBJECT)
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to inkyWHAT screen
    inky_display = import_display(DEFAULT_DISPLAY_OBJECT)
    with inky_display as display:
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
    # Send requests to API endpoints to set data
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to inkyWHAT screen
    inky_display = import_display(DEFAULT_DISPLAY_OBJECT)
    with inky_display as display:
        display.draw_date()
        display.draw_time()
        display.draw_mini_forecast(weather_data)
        display.draw_weather_forecast(weather_data)
        display.draw_forecast_icons(weather_data)


def night() -> None:
    """inky_pi goodnight message main function"""
    # Send requests to API endpoints to set data
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to night inkyWHAT screen
    inky_display = import_display(NIGHT_DISPLAY_OBJECT)
    with inky_display as display:
        display.draw_goodnight(weather_data)


def terminal() -> None:
    """
    Terminal display for inky_pi.
    """
    # Send requests to API endpoints to set data
    train_data: TrainBase = train_model_factory(TRAIN_OBJECT)
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Draw to terminal
    terminal_display_object = DisplayObject(model=DisplayModel.TERMINAL)
    terminal_display: DisplayBase = display_model_factory(terminal_display_object)
    with terminal_display as display:
        display.draw_date()
        display.draw_time()
        display.draw_weather_icon(weather_data.get_icon())
        display.draw_weather_forecast(weather_data)
        display.draw_train_times(train_data)


if __name__ == "__main__":
    configure_logging()
    logger.debug("InkyPi initialized")
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
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(exc)
