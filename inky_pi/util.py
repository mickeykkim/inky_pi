"""Utility functions for inky_pi."""
from loguru import logger


def configure_logging() -> None:
    """See: https://loguru.readthedocs.io/en/stable/api.html"""
    logger.add("inky.log", rotation="5 MB", serialize=True)
