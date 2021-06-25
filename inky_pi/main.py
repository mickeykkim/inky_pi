"""Main Inky_Pi module.

Fetches Train and Weather data and displays on a Raspberry Pi w/InkyWHAT."""
from PIL import Image, ImageDraw

from inky_pi.train.train_control import req_train_data
from inky_pi.view.drawing import (I_BLACK, I_DISPLAY, draw_date_text,
                                  draw_time_text, draw_train_text,
                                  draw_weather_icon, draw_weather_text)
from inky_pi.weather.weather_control import get_weather_icon, req_weather_data

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

    # Set image drawing variables
    img = Image.new('P', (I_DISPLAY.WIDTH, I_DISPLAY.HEIGHT))
    img_draw = ImageDraw.Draw(img)

    # Draw text and weather icon
    draw_date_text(img_draw, 10, 10)
    draw_time_text(img_draw, 300, 10)
    draw_train_text(img_draw, train_data, 10, 60)
    draw_weather_text(img_draw, weather_data, 10, 160)
    draw_weather_icon(img_draw, get_weather_icon(weather_data), 300, 200)

    # Render border, images (w/text) on inky screen and show on display
    I_DISPLAY.set_border(I_BLACK)
    I_DISPLAY.set_image(img)
    I_DISPLAY.show()


if __name__ == "__main__":
    main()
