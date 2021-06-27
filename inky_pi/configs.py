"""Inky_Pi configuration settings.
"""
from environs import Env

_env: Env = Env()
_env.read_env()

# Train constants
T_STATION_FROM: str = _env.str("W_API_KEY", default='maze hill')
"""From (departing) station"""

T_STATION_TO: str = _env.str("T_STATION_TO", default='london bridge')
"""To (arrival) station"""

T_NUM: int = _env.int("T_NUM", default=3)
"""Number of departing trains to fetch"""

# Weather constants; default London
W_LATITUDE: float = _env.float("W_LATITUDE", default=51.5085)
"""Target Latitude"""

W_LONGITUDE: float = _env.float("W_LONGITUDE", default=-0.1257)
"""Target Longitude"""

W_EXCLUDE: str = _env.str("W_EXCLUDE", default='minutely,hourly')
"""Weather data exclude flags"""

# OpenWeatherMap API Key: https://home.openweathermap.org/api_keys
# Keep this in a .env file in project root folder i.e.: W_API_KEY=keyvalue
W_API_KEY: str = _env.str("W_API_KEY", default='keep-in-.env-file')
"""OpenWeatherMap API Key"""
