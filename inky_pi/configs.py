"""Inky_Pi configuration settings.
"""
from environs import Env

_env: Env = Env()
_env.read_env()

TRAIN_MODEL: str = _env.str("TRAIN_MODEL", default="OPEN_LIVE")
"""Train model to use"""

# Train constants
STATION_FROM: str = _env.str("STATION_FROM", default="MZH")
"""From (departing) station"""

STATION_TO: str = _env.str("STATION_TO", default="LBG")
"""To (arrival) station"""

TRAIN_NUMBER: int = _env.int("TRAIN_NUMBER", default=3)
"""Number of departing trains to fetch"""

# Token: https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration
# Keep this in a .env file in project root dir i.e.: TRAIN_API_TOKEN=keyvalue
TRAIN_API_TOKEN: str = _env.str("TRAIN_API_TOKEN", default="keep-in-.env-file")
"""OpenLDBWS API Token"""

TRAIN_MODEL_URL: str = _env.str(
    "TRAIN_MODEL_URL",
    default="http://lite.realtime.nationalrail.co.uk/"
    + "OpenLDBWS/wsdl.aspx?ver=2017-10-01",
)
"""OpenLDBWS API Endpoint"""

WEATHER_MODEL: str = _env.str("WEATHER_MODEL", default="OPEN_WEATHER_MAP")
"""Weather model to use"""

# Weather constants; default London
LATITUDE: float = _env.float("LATITUDE", default=51.5085)
"""Target Latitude"""

LONGITUDE: float = _env.float("LONGITUDE", default=-0.1257)
"""Target Longitude"""

EXCLUDE_FLAGS: str = _env.str("EXCLUDE_FLAGS", default="minutely,hourly")
"""Weather data exclude flags"""

# OpenWeatherMap API Key: https://home.openweathermap.org/api_keys
# Keep this in a .env file in project root dir i.e.: WEATHER_API_TOKEN=keyvalue
WEATHER_API_TOKEN: str = _env.str("WEATHER_API_TOKEN", default="keep-in-.env-file")
"""OpenWeatherMap API Key"""
