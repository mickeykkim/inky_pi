"""
Forms for the flask app
"""
from pathlib import Path

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from inky_pi.configs import InkyColor, Settings
from inky_pi.train.train_base import TrainModel
from inky_pi.util import load_json
from inky_pi.weather.weather_base import WeatherModel

ROOT_DIR = Path(__file__).parent
STATIC_DIR = ROOT_DIR.joinpath("static")
station_crs_data = load_json(STATIC_DIR / "crs_codes.json")
default_config = Settings()


# Ignoring type b/c flask_wtf does not have stubs
class ConfigurationForm(FlaskForm):  # type: ignore[misc]
    """
    Form for environment variables
    """

    inky_color = SelectField(
        label="Inky Display Color",
        description="The color of the Inky display. Options: red, black, yellow.",
        choices=[(color.value, color.value) for color in InkyColor],
        validators=[InputRequired()],
    )
    train_model = SelectField(
        label="Train Model",
        description="The model option to use for train predictions",
        choices=[(model.value, model.value) for model in TrainModel],
        validators=[InputRequired()],
    )
    station_from = SelectField(
        label="Station From",
        description="The departure station",
        choices=[
            (station["crsCode"], station["stationName"]) for station in station_crs_data
        ],
        validators=[InputRequired()],
    )
    station_to = SelectField(
        label="Station To",
        description="The arrival station",
        choices=[
            (station["crsCode"], station["stationName"]) for station in station_crs_data
        ],
        validators=[InputRequired()],
    )
    train_number = IntegerField(
        label="Train Number",
        description="How many upcoming trains to fetch",
        validators=[InputRequired()],
    )
    train_api_token = StringField(
        label="Train API Token",
        description="API token for train service",
        validators=[InputRequired()],
    )
    train_model_url = StringField(
        label="Train Model URL",
        description="Train API URL to fetch data from",
        validators=[InputRequired()],
    )
    weather_model = SelectField(
        label="Weather Model",
        description="Which weather model to use",
        choices=[(model.value, model.value) for model in WeatherModel],
        validators=[InputRequired()],
    )
    latitude = FloatField(
        label="Latitude",
        description="Your latitude for weather data",
        validators=[InputRequired()],
    )
    longitude = FloatField(
        label="Longitude",
        description="Your longitude for weather data",
        validators=[InputRequired()],
    )
    exclude_flags = StringField(
        label="Exclude Flags",
        description=(
            "Exclude some parts of the weather data from the API response as a"
            " comma-delimited list (without spaces). Options: current, minutely,"
            " hourly, daily, alerts."
        ),
        validators=[InputRequired()],
    )
    weather_api_token = StringField(
        label="Weather API Token",
        description="API Token for weather service",
        validators=[InputRequired()],
    )
    flask_debug = BooleanField(
        label="Flask Debug",
        description="Flask debugging flag",
        validators=[InputRequired()],
    )
    flask_testing = BooleanField(
        label="Flask Testing",
        description="Flask testing flag",
        validators=[InputRequired()],
    )
    flask_secret_key = StringField(
        label="Flask Secret Key",
        description="Flask secret key",
        validators=[InputRequired()],
    )
    submit = SubmitField("Update")
