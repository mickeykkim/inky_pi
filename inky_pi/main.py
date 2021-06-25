"""Inky_Pi main module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from PIL import Image, ImageDraw

from inky_pi.train.model_t import req_train_data
from inky_pi.view.drawing import (I_DISPLAY, draw_date_text, draw_time_text,
                                  draw_train_text, draw_weather_icon,
                                  draw_weather_text, render_inky)
from inky_pi.weather.model_w import req_weather_data, get_weather_icon

# Train constants
T_STATION_FROM = 'maze hill'
T_STATION_TO = 'london bridge'
T_NUM_DEPARTURES = 3

# Weather constants
W_LATITUDE = 51.5085
W_LONGITUDE = -0.1257
W_EXCLUDE = 'minutely,hourly'
# Replace the following w/ your OpenWeatherMap API key & keep it secret:
W_API_KEY = ""


def main() -> None:
    """inky_pi main function

    Retrieves train and weather data from API endpoints, generates text and
    weather icon, and draws to inkyWHAT screen.
    """
    # Send requests to API endpoints to set train and weather data
    train_data = req_train_data(T_STATION_FROM, T_STATION_TO, T_NUM_DEPARTURES)
    weather_data = req_weather_data(W_LATITUDE, W_LONGITUDE, W_EXCLUDE,
                                    W_API_KEY)

    # Check for errors in weather response, i.e. API key is invalid (cod==401)
    if 'cod' in weather_data:
        raise ValueError(weather_data['message'])

    # Create image drawing objects
    img = Image.new('P', (I_DISPLAY.WIDTH, I_DISPLAY.HEIGHT))
    img_draw = ImageDraw.Draw(img)

    # Draw text and weather icon on image objects at provided x, y coords
    draw_date_text(img_draw, 10, 10)
    draw_time_text(img_draw, 300, 10)
    draw_train_text(img_draw, train_data, 10, 60)
    draw_weather_text(img_draw, weather_data, True, 10, 160)
    draw_weather_icon(img_draw, get_weather_icon(weather_data), 300, 200)

    # Render drawn image object on Inky display
    render_inky(img)


if __name__ == "__main__":
    main()
