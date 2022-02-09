"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from inky import InkyWHAT  # type: ignore
from loguru import logger

from inky_pi.configs import (EXCLUDE_FLAGS, LATITUDE, LONGITUDE, STATION_FROM,
                             STATION_TO, TRAIN_API_TOKEN, TRAIN_MODEL_URL,
                             TRAIN_NUMBER, WEATHER_API_TOKEN)
from inky_pi.display.inky_draw import InkyDraw  # type: ignore
from inky_pi.helper import (TrainModel, TrainObject, configure_logging,
                            train_model_factory)
from inky_pi.train.train_base import TrainBase  # type: ignore
from inky_pi.weather.open_weather_map import OpenWeatherMap  # type: ignore
from inky_pi.weather.weather_base import ScaleType, WeatherBase  # type: ignore


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    configure_logging()
    logger.debug("InkyPi initialized")
    train_object = TrainObject(model=TrainModel.OPEN_LIVE,
                               station_from=STATION_FROM,
                               station_to=STATION_TO,
                               number=TRAIN_NUMBER,
                               url=TRAIN_MODEL_URL,
                               token=TRAIN_API_TOKEN)

    # Send requests to API endpoints to set data
    train_data: TrainBase = train_model_factory(train_object)

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
