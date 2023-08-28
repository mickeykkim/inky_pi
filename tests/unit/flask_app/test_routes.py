"""
Test the routes of the Flask application
"""
import os

from flask.testing import FlaskClient


def test_index_route(client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid

    Args:
        client:
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


def test_display_env_variables(client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/display' page is requested (GET)
    THEN check the response is valid

    Args:
        client:
    """
    # Define environment variables to be used in the test
    test_latitude = "40.7128"
    test_longitude = "-74.0060"
    test_weather_api_token = "your_weather_api_token"
    test_train_api_token = "your_train_api_token"

    os.environ["LATITUDE"] = test_latitude
    os.environ["LONGITUDE"] = test_longitude
    os.environ["WEATHER_API_TOKEN"] = test_weather_api_token
    os.environ["TRAIN_API_TOKEN"] = test_train_api_token

    response = client.get("/display")
    assert response.status_code == 200
    assert f"{test_latitude}".encode() in response.data
    assert f"{test_longitude}".encode() in response.data
    assert f"{test_weather_api_token}".encode() in response.data
    assert f"{test_train_api_token}".encode() in response.data

    # Clean up: remove environment variables
    del os.environ["LATITUDE"]
    del os.environ["LONGITUDE"]
    del os.environ["WEATHER_API_TOKEN"]
    del os.environ["TRAIN_API_TOKEN"]
