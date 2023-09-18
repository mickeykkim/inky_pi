"""
Test the routes of the Flask application
"""
from unittest.mock import patch

from flask.testing import FlaskClient

TEST_LATITUDE = "-10.0001"
TEST_LONGITUDE = "11.1111"
TEST_WEATHER_API_TOKEN = "test_weather_api_token"
TEST_TRAIN_API_TOKEN = "test_train_api_token"


def test_index_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid

    Args:
        test_client (FlaskClient): Flask test client
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.data


def test_display_route(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/display' page is requested (GET)
    THEN check the response is valid

    Args:
        test_client (FlaskClient): Flask test client
    """
    # Use monkeypatch to temporarily modify environment variables
    with patch("inky_web.routes.get_dot_env") as mock_get_dot_env:
        mock_get_dot_env.return_value = (
            TEST_LATITUDE,
            TEST_LONGITUDE,
            TEST_WEATHER_API_TOKEN,
            TEST_TRAIN_API_TOKEN,
        )

        # Send a GET request to the display route
        response = test_client.get("/display")
        assert response.status_code == 200
        assert f"{TEST_LATITUDE}".encode() in response.data
        assert f"{TEST_LONGITUDE}".encode() in response.data
        assert f"{TEST_WEATHER_API_TOKEN}".encode() in response.data
        assert f"{TEST_TRAIN_API_TOKEN}".encode() in response.data


def test_edit_env_variables_get(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/edit_env' page is requested (GET)
    THEN check the response is valid

    Args:
        test_client(FlaskClient): Flask test client
    """
    # Use dotenv to load environment variables from .env file
    with patch("inky_web.routes.get_dot_env") as mock_get_dot_env:
        mock_get_dot_env.return_value = (
            TEST_LATITUDE,
            TEST_LONGITUDE,
            TEST_WEATHER_API_TOKEN,
            TEST_TRAIN_API_TOKEN,
        )
        # Send a GET request to the edit_env_variables route
        response_get = test_client.get("/edit_env", follow_redirects=True)

        # Check if the response status code is 200 (OK)
        assert response_get.status_code == 200

        # Check if the HTML form is present in the response
        assert b"<form" in response_get.data
        assert f"{TEST_LATITUDE}".encode() in response_get.data
        assert f"{TEST_LONGITUDE}".encode() in response_get.data
        assert f"{TEST_WEATHER_API_TOKEN}".encode() in response_get.data
        assert f"{TEST_TRAIN_API_TOKEN}".encode() in response_get.data


def test_edit_env_variables_post(test_client: FlaskClient) -> None:
    """
    GIVEN a Flask application
    WHEN the '/edit_env' page is requested (POST)
    THEN check the response is valid

    Args:
        test_client(FlaskClient): Flask test client
    """
    with (
        patch("inky_web.routes.EnvVariableForm") as mock_env_variable_form,
        patch("inky_web.routes.set_dot_env") as mock_set_dot_env,
    ):
        # Send a POST request with new form data
        new_data = {
            "latitude": TEST_LATITUDE,
            "longitude": TEST_LONGITUDE,
            "weather_api_token": TEST_WEATHER_API_TOKEN,
            "train_api_token": TEST_TRAIN_API_TOKEN,
        }
        response_post = test_client.post(
            "/edit_env", data=new_data, follow_redirects=True
        )

    assert response_post.status_code == 200
    mock_env_variable_form.assert_called_once_with()
    mock_set_dot_env.assert_called_once()
