"""Tests for utility methods and classes"""
from unittest.mock import Mock, patch

from inky_pi.util import LOG_FILE, LOG_ROTATION, LOG_SERIALIZE, configure_logging


@patch("inky_pi.util.logger.add")
def test_can_successfully_configure_logging(logger_add_mock: Mock) -> None:
    """Test for setting up logging"""
    configure_logging()
    logger_add_mock.assert_called_once_with(
        LOG_FILE, rotation=LOG_ROTATION, serialize=LOG_SERIALIZE
    )
