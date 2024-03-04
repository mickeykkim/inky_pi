"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from enum import Enum, auto
from typing import Dict

from loguru import logger

from inky_pi import __version__
from inky_pi.configs import InkyColor, Settings
from inky_pi.display.display_base import DisplayModel, DisplayOutput
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

config = Settings()

# Define objects to be used in fetching data
TRAIN_OBJECT = TrainObject(
    model=TrainModel[config.TRAIN_MODEL],
    station_from=config.STATION_FROM,
    station_to=config.STATION_TO,
    number=config.TRAIN_NUMBER,
    url=config.TRAIN_MODEL_URL,
    token=config.TRAIN_API_TOKEN,
)

WEATHER_OBJECT = WeatherObject(
    model=WeatherModel[config.WEATHER_MODEL],
    latitude=config.LATITUDE,
    longitude=config.LONGITUDE,
    exclude_flags=config.EXCLUDE_FLAGS,
    weather_api_token=config.WEATHER_API_TOKEN,
)


class DisplayOption(Enum):
    """Enum of display options"""

    TRAIN = auto()
    WEATHER = auto()
    NIGHT = auto()


DEFAULT_COLOR = InkyColor.BLACK.value
OUTPUT_DISPATCH_TABLE: Dict[str, DisplayOutput] = {
    "INKY": DisplayOutput(model=DisplayModel.INKY, base_color=DEFAULT_COLOR),
    "TERMINAL": DisplayOutput(model=DisplayModel.TERMINAL, base_color=DEFAULT_COLOR),
    "DESKTOP": DisplayOutput(model=DisplayModel.DESKTOP, base_color=DEFAULT_COLOR),
}


def _parse_args(args: list[str]) -> Namespace:
    """Parses the command line arguments and returns the parsed arguments.

    Returns:
        Namespace: Parsed command line arguments.
    """
    parser = ArgumentParser(
        description=(
            "Displays train, weather, and/or goodnight screen data to chosen output"
        ),
    )
    parser.add_argument(
        "-o",
        "--option",
        help="Display option (train, weather, night)",
        type=str,
        default="train",
        choices=[option.name.lower() for option in DisplayOption],
    )
    parser.add_argument(
        "-m",
        "--output",
        help="Output destination (inky, terminal, desktop)",
        type=str,
        default="inky",
        choices=[model.name.lower() for model in DisplayModel],
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Inky_Pi version",
        action="version",
        version="%(prog)s " + __version__,
    )
    parser.add_argument(
        "--dry-run",
        help="Dry run",
        action="store_true",
        default=False,
    )
    return parser.parse_args(args)


def display_data(option: DisplayOption, output: DisplayOutput) -> None:
    """inky_pi weather with train function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.

    Args:
        option (DisplayOption): Display Option enum (TRAIN, WEATHER, NIGHT)
        output (DisplayOutput): Display Output dataclass (INKY | TERMINAL | DESKTOP)
    """
    # Weather data is always used
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    with import_display(output) as display:
        logger.debug(
            "InkyPi displaying option: {option} on output: {output}",
            option=option.name.lower(),
            output=output.model.name.lower(),
        )
        if option == DisplayOption.NIGHT:
            output.base_color = config.INKY_COLOR
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
            # Train data is only queried if the option is TRAIN
            train_data: TrainBase = train_model_factory(TRAIN_OBJECT)
            display.draw_train_times(train_data, config.TRAIN_NUMBER)
        elif option == DisplayOption.WEATHER:
            display.draw_forecast_icons(weather_data)


def main() -> None:
    """The entry point for the program. It parses the command line arguments and calls
    the appropriate display function and output option based on the arguments.
    """
    configure_logging()
    logger.debug("InkyPi main initialized")
    args: Namespace = _parse_args(sys.argv[1:])
    if args.dry_run:
        logger.debug(
            "Dry run: option = {option} / output = {output}",
            option=args.option.lower(),
            output=args.output.lower(),
        )
        return
    try:
        display_data(
            DisplayOption[args.option.upper()],
            OUTPUT_DISPATCH_TABLE[args.output.upper()],
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(exc)
        raise


if __name__ == "__main__":
    main()
