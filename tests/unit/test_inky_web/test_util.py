"""
Test the util.py file in the flask_app directory
"""

from inky_web.util import get_dot_env, set_dot_env

from .conftest import (
    TEMP_ENV_LATITUDE,
    TEMP_ENV_LONGITUDE,
    TEMP_ENV_TRAIN_API_TOKEN,
    TEMP_ENV_WEATHER_API_TOKEN,
)


def test_get_dot_env(temp_env_file: str) -> None:
    """
    Test the get_dot_env function

    Args:
        temp_env_file (NamedTemporaryFile): Temporary .env file
    """
    settings = get_dot_env(temp_env_file)

    assert settings["LATITUDE"] == TEMP_ENV_LATITUDE
    assert settings["LONGITUDE"] == TEMP_ENV_LONGITUDE
    assert settings["WEATHER_API_TOKEN"] == TEMP_ENV_WEATHER_API_TOKEN
    assert settings["TRAIN_API_TOKEN"] == TEMP_ENV_TRAIN_API_TOKEN


def test_set_dot_env(temp_env_file: str) -> None:
    """
    Test the set_dot_env function

    Args:
        temp_env_file (NamedTemporaryFile): Temporary .env file
    """
    original_settings = get_dot_env(temp_env_file)

    test_latitude = "1.01"
    test_longitude = "-10.1"
    test_weather_api_token = "test_token123"
    test_train_api_token = "test_token456"

    assert original_settings["LATITUDE"] != test_latitude
    assert original_settings["LONGITUDE"] != test_longitude
    assert original_settings["WEATHER_API_TOKEN"] != test_weather_api_token
    assert original_settings["TRAIN_API_TOKEN"] != test_train_api_token

    new_settings = {
        "LATITUDE": test_latitude,
        "LONGITUDE": test_longitude,
        "WEATHER_API_TOKEN": test_weather_api_token,
        "TRAIN_API_TOKEN": test_train_api_token,
    }

    set_dot_env(settings=new_settings, dotenv_path=temp_env_file)

    # Check if the values were updated
    updated_settings = get_dot_env(temp_env_file)

    assert updated_settings["LATITUDE"] == test_latitude
    assert updated_settings["LONGITUDE"] == test_longitude
    assert updated_settings["WEATHER_API_TOKEN"] == test_weather_api_token
    assert updated_settings["TRAIN_API_TOKEN"] == test_train_api_token
