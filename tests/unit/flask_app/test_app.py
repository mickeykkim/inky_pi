"""
Test the Flask app.
"""
import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from flask import Flask

from flask_app.app import main, parse_args

from .conftest import TEST_CONFIG


def test_create_app_without_config(app: Flask) -> None:
    """
    GIVEN a Flask application
    WHEN the app is created without a config
    THEN check the debug and testing flags are set correctly

    Args:
        app: Flask fixture without config
    """
    load_dotenv()
    assert app.config["DEBUG"] == bool(os.getenv("FLASK_DEBUG"))
    assert app.config["TESTING"] == bool(os.getenv("FLASK_TESTING"))
    assert app.config["SECRET_KEY"] == os.getenv("FLASK_SECRET_KEY", "")


def test_create_app_with_config(test_app: Flask) -> None:
    """
    GIVEN a Flask application
    WHEN the app is created with test config
    THEN check the debug and testing flags are set correctly

    Args:
        test_app: Flask fixture with test config
    """
    assert test_app.config["DEBUG"] == TEST_CONFIG.DEBUG
    assert test_app.config["TESTING"] == TEST_CONFIG.TESTING
    assert test_app.config["SECRET_KEY"] == TEST_CONFIG.SECRET_KEY


@pytest.mark.parametrize(
    "args, expected_host, expected_port",
    [
        ([], "localhost", 5000),  # Default values
        (
            ["--host", "example.com", "--port", "8080"],
            "example.com",
            8080,
        ),  # Custom values
    ],
)
def test_parse_args(args: list[str], expected_host: str, expected_port: int) -> None:
    """
    GIVEN a list of command line arguments
    WHEN the arguments are parsed
    THEN check the host and port are set correctly

    Args:
        args (list[str]): List of command line arguments
        expected_host (str): Expected host
        expected_port (int): Expected port
    """
    parsed_args = parse_args(args)
    assert parsed_args.host == expected_host
    assert parsed_args.port == expected_port


def test_main() -> None:
    """
    GIVEN a mocked parse_args function
    WHEN the main function is called
    THEN check the parse_args function is called correctly
    """
    cl_arguments = ["--host", "example.com", "--port", "8080"]
    with (
        patch("flask_app.app.parse_args") as mock_parse_args,
        patch("flask_app.app.create_app") as mock_create_app,
    ):
        main(cl_arguments=cl_arguments)
        mock_parse_args.assert_called_once_with(cl_arguments)
        mock_create_app.assert_called_once()
