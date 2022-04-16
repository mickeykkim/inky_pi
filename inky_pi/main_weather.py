"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
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
from inky_pi.helper import WeatherModel, WeatherObject, weather_model_factory
from inky_pi.util import configure_logging
from inky_pi.weather.weather_base import ScaleType, WeatherBase

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
    weather_data: WeatherBase = weather_model_factory(WEATHER_OBJECT)

    # Set the display object configured with specified Inky display model
    display = InkyDraw(InkyWHAT("black"))

    # Draw text and weather icon on display object at specified x, y coords
    display.draw_date(10, 5)
    display.draw_time(297, 5)
    display.draw_weather_forecast(weather_data, ScaleType.CELSIUS, 10, 45)
    display.draw_weather_icon(weather_data.get_icon(), 300, 85)

    # Render display object on Inky display screen
    display.render_screen()


if __name__ == "__main__":
    main()
