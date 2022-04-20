"""Inky_Pi main weather module.

Fetches extended weather data and displays on a Raspberry Pi w/InkyWHAT."""
# pylint: disable=duplicate-code
from inky import InkyWHAT  # type: ignore
from loguru import logger

from inky_pi.configs import (
    EXCLUDE_FLAGS,
    LATITUDE,
    LONGITUDE,
    WEATHER_API_TOKEN,
    WEATHER_MODEL,
)
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.util import (
    WeatherModel,
    WeatherObject,
    configure_logging,
    weather_model_factory,
)
from inky_pi.weather.weather_base import WeatherBase

WEATHER_OBJECT = WeatherObject(
    model=WeatherModel[WEATHER_MODEL],
    latitude=LATITUDE,
    longitude=LONGITUDE,
    exclude_flags=EXCLUDE_FLAGS,
    weather_api_token=WEATHER_API_TOKEN,
)


def main() -> None:
    """inky_pi main function

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


if __name__ == "__main__":
    main()
