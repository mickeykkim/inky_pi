"""Tests for utility methods and classes"""
from unittest.mock import Mock, patch

import pytest

from inky_pi.train.train_base import TrainModel, TrainObject
from inky_pi.util import (
    LOG_FILE,
    LOG_ROTATION,
    LOG_SERIALIZE,
    configure_logging,
    train_model_factory,
    weather_model_factory,
)
from inky_pi.weather.weather_base import WeatherModel, WeatherObject


@patch("inky_pi.util.logger.add")
def test_can_successfully_configure_logging(logger_add_mock: Mock) -> None:
    """Test for setting up logging"""
    configure_logging()
    logger_add_mock.assert_called_once_with(
        LOG_FILE, rotation=LOG_ROTATION, serialize=LOG_SERIALIZE
    )


def test_that_train_model_factory_with_invalid_model_raises_exception() -> None:
    """Test for invalid train model"""
    with pytest.raises(SystemExit):
        train_model_factory(
            TrainObject(
                TrainModel.OPEN_LIVE,
                "INVALID",
                "INVALID",
                -1,
                "http://www.com",
                "INVALID",
            )
        )


def test_that_weather_model_factory_with_invalid_model_raises_exception() -> None:
    """Test for invalid weather model"""
    with pytest.raises(SystemExit):
        weather_model_factory(
            WeatherObject(WeatherModel.OPEN_WEATHER_MAP, -1, -1, "INVALID", "INVALID")
        )
