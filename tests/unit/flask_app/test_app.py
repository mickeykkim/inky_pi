"""
Test the Flask app.
"""
from flask import Flask


def test_create_app(test_app: Flask) -> None:
    """
    GIVEN a Flask application
    WHEN the app is created
    THEN check the debug and testing flags are set correctly

    Args:
        test_app:
    """
    assert test_app.config["DEBUG"] is True
    assert test_app.config["TESTING"] is True
