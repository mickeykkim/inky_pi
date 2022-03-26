"""Utility functions for inky_pi."""


import io

from loguru import logger


def configure_logging() -> None:
    """See: https://loguru.readthedocs.io/en/stable/api.html"""
    logger.add("inky.log", rotation="5 MB", serialize=True)


def is_raspberrypi() -> bool:
    """Check if we are running on a Raspberry Pi.

    Returns:
        True if we are running on a Raspberry Pi, False otherwise.
    """
    try:
        with io.open(
            "/sys/firmware/devicetree/base/model", "r", encoding="utf-8"
        ) as file:
            if "raspberry pi" in file.read().lower():
                return True
    except FileNotFoundError:
        return False
    return False
