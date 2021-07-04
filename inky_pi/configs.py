"""Inky_Pi configuration settings.
"""
from environs import Env

_env: Env = Env()
_env.read_env()

T_MODEL: str = _env.str("T_MODEL", default='openldbws')
"""Train model to use"""

# Train constants
T_STATION_FROM: str = _env.str("T_STATION_FROM", default='MZH')
"""From (departing) station"""

T_STATION_TO: str = _env.str("T_STATION_TO", default='LBG')
"""To (arrival) station"""

T_NUM: int = _env.int("T_NUM", default=3)
"""Number of departing trains to fetch"""

# Token: https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration
# Keep this in a .env file in project root folder i.e.: T_LDB_TOKEN=keyvalue
T_LDB_TOKEN: str = _env.str("T_LDB_TOKEN", default='keep-in-.env-file')
"""OpenLDBWS API Token"""

T_WSDL: str = _env.str("T_WDSL",
                       default='http://lite.realtime.nationalrail.co.uk/' +
                       'OpenLDBWS/wsdl.aspx?ver=2017-10-01')
"""OpenLDBWS API Endpoint"""

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
