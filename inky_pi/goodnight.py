"""Goodnight message after hours"""
from inky import InkyWHAT  # type: ignore

from inky_pi.configs import (EXCLUDE_FLAGS, LATITUDE, LONGITUDE,
                             WEATHER_API_TOKEN)
from inky_pi.display.inky_draw import InkyDraw  # type: ignore
from inky_pi.weather.open_weather_map import OpenWeatherMap  # type: ignore
from inky_pi.weather.weather_base import ScaleType, WeatherBase  # type: ignore


def main() -> None:
    """inky_pi goodnight message main function
    """
    weather_data: WeatherBase = OpenWeatherMap(LATITUDE, LONGITUDE, EXCLUDE_FLAGS,
                                               WEATHER_API_TOKEN)

    # Set the display object configured with specified Inky display model
    display = InkyDraw(InkyWHAT('black'))
    display.draw_goodnight(weather_data, ScaleType.celsius)
    display.render_screen()


if __name__ == "__main__":
    main()
