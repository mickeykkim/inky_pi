"""
Test the util.py file in the flask_app directory
"""
from flask_app.util import get_dot_env, set_dot_env

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
    latitude, longitude, weather_api_token, train_api_token = get_dot_env(temp_env_file)

    assert latitude == TEMP_ENV_LATITUDE
    assert longitude == TEMP_ENV_LONGITUDE
    assert weather_api_token == TEMP_ENV_WEATHER_API_TOKEN
    assert train_api_token == TEMP_ENV_TRAIN_API_TOKEN


def test_set_dot_env(temp_env_file: str) -> None:
    """
    Test the set_dot_env function

    Args:
        temp_env_file (NamedTemporaryFile): Temporary .env file
    """
    (
        original_latitude,
        original_longitude,
        original_weather_api_token,
        original_train_api_token,
    ) = get_dot_env(temp_env_file)

    test_latitude = "1.01"
    test_longitude = "-10.1"
    test_weather_api_token = "test_token123"
    test_train_api_token = "test_token456"

    assert original_latitude != test_latitude
    assert original_longitude != test_longitude
    assert original_weather_api_token != test_weather_api_token
    assert original_train_api_token != test_train_api_token

    set_dot_env(
        latitude=test_latitude,
        longitude=test_longitude,
        weather_api_token=test_weather_api_token,
        train_api_token=test_train_api_token,
        dotenv_path=temp_env_file,
    )

    # Check if the values were updated
    (
        updated_latitude,
        updated_longitude,
        updated_weather_api_token,
        updated_train_api_token,
    ) = get_dot_env(temp_env_file)

    assert updated_latitude == test_latitude
    assert updated_longitude == test_longitude
    assert updated_weather_api_token == test_weather_api_token
    assert updated_train_api_token == test_train_api_token
