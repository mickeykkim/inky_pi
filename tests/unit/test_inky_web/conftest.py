"""
Configuration and fixtures for tests
"""

import os
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from inky_web.__main__ import AppConfig, create_app

TEST_CONFIG = AppConfig()
TEST_CONFIG.DEBUG = True
TEST_CONFIG.TESTING = True
TEST_CONFIG.SECRET_KEY = "test_secret_key"

TEMP_ENV_LATITUDE = "55.678"
TEMP_ENV_LONGITUDE = "-88.901"
TEMP_ENV_WEATHER_API_TOKEN = "new_token123"
TEMP_ENV_TRAIN_API_TOKEN = "new_token456"


@pytest.fixture(name="app", scope="module")
def app_fixture() -> Flask:
    """
    Create the Flask app fixture without the test configuration

    Returns:
        Flask: Flask app object
    """
    app_object = create_app()
    return app_object


@pytest.fixture(name="test_app", scope="module")
def test_app_fixture() -> Flask:
    """
    Create the Flask app fixture with the test configuration

    Returns:
        Flask: Flask app object
    """

    test_app_object = create_app(TEST_CONFIG)
    return test_app_object


@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    """
    Create the Flask test client without the test configuration

    Args:
        app:

    Returns:
        Flask.test_client: Flask test client
    """
    return app.test_client()


@pytest.fixture(scope="module")
def test_client(test_app: Flask) -> FlaskClient:
    """
    Create the Flask test client with the test configuration

    Args:
        test_app:

    Returns:
        Flask.test_client: Flask test client
    """
    return test_app.test_client()


@pytest.fixture
def temp_env_file() -> Generator[str, None, None]:
    """
    Create a temporary .env file for testing

    Returns:
        Generator[str, None, None]: Yielded temporary .env file
    """
    with NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write(
            f"LATITUDE={TEMP_ENV_LATITUDE}\n"
            f"LONGITUDE={TEMP_ENV_LONGITUDE}\n"
            f"WEATHER_API_TOKEN={TEMP_ENV_WEATHER_API_TOKEN}\n"
            f"TRAIN_API_TOKEN={TEMP_ENV_TRAIN_API_TOKEN}\n"
        )
    yield temp_file.name
    # Clean up by removing the temporary .env file
    os.remove(temp_file.name)
