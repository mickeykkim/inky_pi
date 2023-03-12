"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
import sys
from argparse import ArgumentParser, Namespace
from enum import Enum, auto
from typing import Dict

from loguru import logger

from inky_pi.__init__ import __version__  # type: ignore
from inky_pi.configs import (
    EXCLUDE_FLAGS,
    INKY_COLOR,
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
from inky_pi.display.display_base import DisplayModel, DisplayObject
from inky_pi.train.train_base import TrainBase, TrainModel, TrainObject
from inky_pi.util import (
    configure_logging,
    import_display,
    train_model_factory,
    weather_model_factory,
)
from inky_pi.weather.weather_base import (
    ScaleType,
    WeatherBase,
    WeatherModel,
    WeatherObject,
)

# Define objects to be used in fetching data
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


class DisplayOption(Enum):
    """Enum of display options"""

    TRAIN = auto()
    WEATHER = auto()
    NIGHT = auto()


OUTPUT_HANDLER: Dict[str, DisplayObject] = {
    "inky": DisplayObject(model=DisplayModel.INKY_WHAT, base_color="black"),
    "terminal": DisplayObject(model=DisplayModel.TERMINAL),
    "desktop": DisplayObject(model=DisplayModel.DESKTOP),
}


def _parse_args(args) -> Namespace:
    """Parses the command line arguments and returns the parsed arguments.

    Returns:
        Namespace: Parsed command line arguments.
    """
    parser = ArgumentParser(
        description="Displays train and weather data to various outputs",
    )
    parser.add_argument(
        "-o",
        "--option",
        help="Display option (train, weather, night)",
        type=str,
        default="train",
    )
    parser.add_argument(
        "-m",
        "--output",
        help="Output source (inky, terminal, desktop)",
        type=str,
        default="inky",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Inky_Pi version",
        action="version",
        version="%(prog)s " + __version__,
    )
    return parser.parse_args(args)


def display_data(option: DisplayOption, output: DisplayObject) -> None:
    """inky_pi weather with train function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.

    Args:
        option (DisplayOption): Display option (train, weather, night)
        output (DisplayObject): Display object (inkyWHAT, terminal, desktop)
    """
    output.base_color = INKY_COLOR if option == DisplayOption.NIGHT else "black"

    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)
    with import_display(output) as display:
        if option == DisplayOption.NIGHT:
            display.draw_goodnight(weather_data)
            return

        display.draw_date()
        display.draw_time()
        display.draw_weather_icon(weather_data.get_icon())
        display.draw_weather_forecast(
            weather_data,
            ScaleType.CELSIUS,
            disp_tomorrow=bool(option == DisplayOption.TRAIN),
        )
        if option == DisplayOption.TRAIN:
            train_data: TrainBase = train_model_factory(TRAIN_OBJECT)
            display.draw_train_times(train_data, TRAIN_NUMBER)
        elif option == DisplayOption.WEATHER:
            display.draw_forecast_icons(weather_data)


def main() -> None:
    """The entry point for the program. It parses the command line arguments and calls
    the appropriate display function and output option based on the arguments.
    """
    configure_logging()
    logger.debug("InkyPi main initialized")
    args: Namespace = _parse_args(sys.argv[1:])
    try:
        display_data(
            DisplayOption[args.option.upper()], OUTPUT_HANDLER[args.output.lower()]
        )
    except KeyError:
        logger.error(
            f'Invalid display/output specified: "{args.display}"/"{args.output}"'
        )
        raise
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(exc)
        raise


if __name__ == "__main__":
    main()
