"""
Utility functions
"""
from __future__ import annotations

from dotenv import dotenv_values, set_key


def get_dot_env(dotenv_path: str = ".env") -> tuple[str | None, ...]:
    """
    Get the environment variables from the .env file

    Args:
        dotenv_path (str): .env file

    Returns:
        tuple[str, ...]: Tuple of environment variables
    """
    dot_env = dotenv_values(dotenv_path)
    latitude = dot_env.get("LATITUDE", "")
    longitude = dot_env.get("LONGITUDE", "")
    weather_api_token = dot_env.get("WEATHER_API_TOKEN", "")
    train_api_token = dot_env.get("TRAIN_API_TOKEN", "")

    return latitude, longitude, weather_api_token, train_api_token


def set_dot_env(
    *,
    latitude: str,
    longitude: str,
    weather_api_token: str,
    train_api_token: str,
    dotenv_path: str = ".env",
) -> None:
    """
    Set the environment variables to the .env file

    Args:
        latitude (str): Latitude
        longitude (str): Longitude
        weather_api_token (str): Weather API token
        train_api_token (str): Train API token
        dotenv_path (str): .env file
    """
    set_key(dotenv_path, "LATITUDE", latitude)
    set_key(dotenv_path, "LONGITUDE", longitude)
    set_key(dotenv_path, "WEATHER_API_TOKEN", weather_api_token)
    set_key(dotenv_path, "TRAIN_API_TOKEN", train_api_token)
