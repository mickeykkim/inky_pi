"""
Configuration settings for the inky_pi app.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the inky_pi app.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    INKY_COLOR: str = Field(default="yellow")
    TRAIN_MODEL: str = Field(default="OPEN_LIVE")
    STATION_FROM: str = Field(default="BHO")
    STATION_TO: str = Field(default="WMW")
    TRAIN_NUMBER: int = Field(default=3)
    TRAIN_API_TOKEN: str = Field(default="keep-in-.env-file")
    TRAIN_MODEL_URL: str = Field(
        default=(
            "http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01"
        ),
    )
    WEATHER_MODEL: str = Field(default="OPEN_WEATHER_MAP")
    LATITUDE: float = Field(default=51.5085)
    LONGITUDE: float = Field(default=-0.1257)
    EXCLUDE_FLAGS: str = Field(default="minutely,hourly")
    WEATHER_API_TOKEN: str = Field(default="keep-in-.env-file")
    FLASK_DEBUG: bool = Field(default=False)
    FLASK_TESTING: bool = Field(default=False)
    FLASK_SECRET_KEY: str = Field(default="keep-in-.env-file")
