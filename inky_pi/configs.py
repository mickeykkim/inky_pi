"""
Configuration settings for the inky_pi app.

For TRAIN_API_TOKEN and WEATHER_API_TOKEN, you can get these by signing up for
free accounts at the following links:

    * https://lite.realtime.nationalrail.co.uk/OpenLDBWSRegistration/
    * https://openweathermap.org/api

For FLASK_SECRET_KEY, you can generate a secret key by running the following
command in a Python shell:

    >>> import secrets
    >>> secrets.token_hex(16)
"""
from enum import Enum
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from inky_pi.train.train_base import TrainModel
from inky_pi.util import load_json
from inky_pi.weather.weather_base import WeatherModel

ROOT_DIR = Path(__file__).parent.parent
STATIC_DIR = ROOT_DIR.joinpath("inky_web/static")


class InkyColor(Enum):
    """Enum of inky display color options"""

    BLACK = "black"
    YELLOW = "yellow"
    RED = "red"


class Settings(BaseSettings):
    """
    Configuration settings for the inky_pi app.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    INKY_COLOR: str = Field(
        default=InkyColor.YELLOW,
        title="Inky Display Color",
        description="The color of the Inky display. Options: red, black, yellow.",
    )
    TRAIN_MODEL: TrainModel = Field(
        default=TrainModel.OPEN_LIVE,
        title="Train Model",
        description=(
            "The model option to use for train predictions."
            f" Options: {list(TrainModel)}."
        ),
    )
    STATION_FROM: str = Field(
        default="BHO",
        title="Station From",
        description="The departure station in CRS abbreviation format",
    )
    STATION_TO: str = Field(
        default="WMW",
        title="Station To",
        description="The arrival station in CRS abbreviation format",
    )
    TRAIN_NUMBER: int = Field(
        default=3,
        title="Train Number",
        description="How many upcoming trains to fetch",
    )
    TRAIN_API_TOKEN: str = Field(
        default="keep-in-.env-file",
        title="Train API Token",
        description="API token for train service",
    )
    TRAIN_MODEL_URL: str = Field(
        default=(
            "http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01"
        ),
        title="Train Model URL",
        description="Train API URL to fetch data from",
    )
    WEATHER_MODEL: WeatherModel = Field(
        default=WeatherModel.OPEN_WEATHER_MAP,
        title="Weather Model",
        description=f"Which weather model to use. Options: {list(WeatherModel)}.",
    )
    LATITUDE: float = Field(
        default=51.5085,
        title="Latitude",
        description="Your latitude for weather data",
    )
    LONGITUDE: float = Field(
        default=-0.1257,
        title="Longitude",
        description="Your longitude for weather data",
    )
    EXCLUDE_FLAGS: str = Field(
        default="minutely,hourly",
        title="Exclude Flags",
        description=(
            "Exclude some parts of the weather data from the API response as a"
            " comma-delimited list (without spaces). Options: current, minutely,"
            " hourly, daily, alerts."
        ),
    )
    WEATHER_API_TOKEN: str = Field(
        default="keep-in-.env-file",
        title="Weather API Token",
        description="API Token for weather service",
    )
    FLASK_DEBUG: bool = Field(
        default=True,
        title="Flask Debug",
        description="Flask debugging flag",
    )
    FLASK_TESTING: bool = Field(
        default=True,
        title="Flask Testing",
        description="Flask testing flag",
    )
    FLASK_SECRET_KEY: str = Field(
        default="keep-in-.env-file",
        title="Flask Secret Key",
        description="Flask secret key",
    )

    @field_validator("LATITUDE")
    @classmethod
    def _check_latitude_range(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @field_validator("LONGITUDE")
    @classmethod
    def _check_longitude_range(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("Longitude must be between -90 and 90")
        return value

    @field_validator("EXCLUDE_FLAGS")
    @classmethod
    def _check_exclude_flags(cls, value: str) -> str:
        valid_flags = {"current", "minutely", "hourly", "daily", "alerts"}
        flags = value.split(",")
        invalid_flags = [flag for flag in flags if flag not in valid_flags]

        if invalid_flags:
            raise ValueError(
                f"Invalid flags found: {', '.join(invalid_flags)}."
                f" Valid options are: {', '.join(valid_flags)}"
            )
        return value

    @field_validator("STATION_FROM", "STATION_TO")
    @classmethod
    def _check_station_code(cls, value: str) -> str:
        station_crs_data = load_json(STATIC_DIR.joinpath("crs_codes.json"))
        valid_crs_codes = [station["crsCode"] for station in station_crs_data]

        if value not in valid_crs_codes:
            raise ValueError(
                f"Invalid CRS code: {value}."
                f" Valid options are: {', '.join(valid_crs_codes)}"
            )
        return value
