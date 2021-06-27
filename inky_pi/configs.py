"""Inky_Pi configuration settings.
"""
from environs import Env

_env: Env = Env()
_env.read_env()

OPENWEATHER_KEY: str = _env.str("OPENWEATHER_KEY", default='replace-me')
"""OpenWeatherMap API Key"""
