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

from inky_pi.__main__ import InkyColor
from inky_pi.train.train_base import TrainModel
from inky_pi.weather.weather_base import WeatherModel
from inky_web.util import get_crs_codes

ROOT_DIR = Path(__file__).parent
STATIC_DIR = ROOT_DIR.joinpath("static")


station_crs_codes = get_crs_codes(STATIC_DIR / "crs_codes.json")


# Ignoring type b/c flask_wtf does not have stubs
class ConfigurationForm(FlaskForm):  # type: ignore[misc]
    """
    Form for environment variables
    """

    inky_color = SelectField(
        "Inky Display Color",
        choices=[(color.value, color.value) for color in InkyColor],
        validators=[InputRequired()],
    )
    train_model = SelectField(
        "Train Model",
        choices=[(model.name, model.name) for model in TrainModel],
        validators=[InputRequired()],
    )
    station_from = SelectField(
        "Station From",
        choices=[
            (station["crsCode"], station["stationName"])
            for station in station_crs_codes
        ],
        validators=[InputRequired()],
    )
    station_to = SelectField(
        "Station To",
        choices=[
            (station["crsCode"], station["stationName"])
            for station in station_crs_codes
        ],
        validators=[InputRequired()],
    )
    train_number = IntegerField("Train Number", validators=[InputRequired()])
    train_api_token = StringField("Train API Token", validators=[InputRequired()])
    train_model_url = StringField("Train Model URL", validators=[InputRequired()])
    weather_model = SelectField(
        "Weather Model",
        choices=[(model.name, model.name) for model in WeatherModel],
        validators=[InputRequired()],
    )
    latitude = FloatField("Latitude", validators=[InputRequired()])
    longitude = FloatField("Longitude", validators=[InputRequired()])
    exclude_flags = StringField("Exclude Flags", validators=[InputRequired()])
    weather_api_token = StringField("Weather API Token", validators=[InputRequired()])
    flask_debug = BooleanField("Flask Debug", validators=[InputRequired()])
    flask_testing = BooleanField("Flask Testing", validators=[InputRequired()])
    flask_secret_key = StringField("Flask Secret Key", validators=[InputRequired()])
    submit = SubmitField("Update")
