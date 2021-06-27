"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from inky import InkyWHAT  # type: ignore

from inky_pi.configs import OPENWEATHER_KEY
from inky_pi.train.t_model import TrainModel  # type: ignore
from inky_pi.view.inky_draw import InkyDraw  # type: ignore
from inky_pi.weather.w_model import ScaleType, WeatherModel  # type: ignore

# Train constants
T_STATION_FROM = 'maze hill'
T_STATION_TO = 'london bridge'
T_NUM = 3

# Weather constants
W_LATITUDE = 51.5085
W_LONGITUDE = -0.1257
W_EXCLUDE = 'minutely,hourly'
# Replace the following w/ your OpenWeatherMap API key string & keep it secret:
W_API_KEY = OPENWEATHER_KEY


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set data
    train_data = TrainModel(T_STATION_FROM, T_STATION_TO, T_NUM)
    weather_data = WeatherModel(W_LATITUDE, W_LONGITUDE, W_EXCLUDE, W_API_KEY)

    # Set the display object configured with specified Inky display model
    display = InkyDraw(InkyWHAT('black'))

    # Draw text and weather icon on display object at specified x, y coords
    display.draw_date_text(10, 10)
    display.draw_time_text(300, 10)
    display.draw_train_text(train_data, T_NUM, 10, 60)
    display.draw_weather_text(weather_data, ScaleType.celsius, 10, 160)
    display.draw_weather_icon(weather_data.get_icon(), 300, 200)

    # Render display object on Inky display screen
    display.render_screen()


if __name__ == "__main__":
    main()
