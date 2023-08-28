"""
Configuration and fixtures for tests
"""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_app.app import create_app


class TestConfig:
    """
    Test configuration object
    """

    DEBUG = True
    TESTING = True


@pytest.fixture(name="test_app", scope="module")
def test_app_fixture() -> Flask:
    """
    Create the Flask app

    Returns:
        Flask: Flask app object
    """
    test_app_object = create_app(TestConfig())
    return test_app_object


@pytest.fixture(scope="module")
def client(test_app: Flask) -> FlaskClient:
    """
    Create the Flask test client

    Args:
        test_app:

    Returns:
        Flask.test_client: Flask test client
    """
    return test_app.test_client()
