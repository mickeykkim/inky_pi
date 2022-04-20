"""Goodnight message after hours"""
from inky import InkyWHAT  # type: ignore
from loguru import logger

from inky_pi.configs import EXCLUDE_FLAGS, LATITUDE, LONGITUDE, WEATHER_API_TOKEN
from inky_pi.display.inky_draw import InkyDraw
from inky_pi.util import configure_logging
from inky_pi.weather.open_weather_map import OpenWeatherMap
from inky_pi.weather.weather_base import WeatherBase


def main() -> None:
    """inky_pi goodnight message main function"""
    weather_data: WeatherBase = OpenWeatherMap(
        LATITUDE, LONGITUDE, EXCLUDE_FLAGS, WEATHER_API_TOKEN
    )

    configure_logging()
    logger.debug("InkyPi goodnight")

    with InkyDraw(InkyWHAT("yellow")) as display:
        display.draw_goodnight(weather_data)


if __name__ == "__main__":
    main()
