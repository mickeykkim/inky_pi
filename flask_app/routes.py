"""
Routes for flask app
"""
import os

from dotenv import load_dotenv
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)
config_bp = Blueprint("config", __name__)


load_dotenv()


@main_bp.route("/")
def index() -> str:
    """
    Index route

    Returns:
        str: Index page
    """
    return render_template("index.html")


@config_bp.route("/display")
def display_env() -> str:
    """
    Display environment variables

    Returns:
        str: Environment variables
    """
    latitude = os.getenv("LATITUDE")
    longitude = os.getenv("LONGITUDE")
    weather_api_token = os.getenv("WEATHER_API_TOKEN")
    train_api_token = os.getenv("TRAIN_API_TOKEN")

    return render_template(
        "env_load.html",
        latitude=latitude,
        longitude=longitude,
        weather_api_token=weather_api_token,
        train_api_token=train_api_token,
    )
