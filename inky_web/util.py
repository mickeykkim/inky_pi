"""
Utility functions
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dotenv import dotenv_values, set_key

from inky_pi.configs import Settings

config = Settings()


def get_crs_codes(crs_codes_file: Path | str) -> Any:
    """
    Get all station names and their CRS codes

    Args:
        crs_codes_file (Path | str): Path to the CRS codes file

    Returns:
        dict[str, str]: Dictionary of station names and their CRS codes
    """
    with open(crs_codes_file, "r", encoding="utf-8") as file:
        return json.load(file)


def get_dot_env(dotenv_path: str = ".env") -> dict[str, str | float | int | bool]:
    """
    Get all settings and their values from the .env file, with defaults Settings

    Args:
        dotenv_path (str): .env file path

    Returns:
        dict: Dictionary of settings and their values
    """
    dot_env = dotenv_values(dotenv_path)
    settings_dict = {}

    for setting in config.__annotations__:
        setting_value = dot_env.get(setting)
        if setting_value is None:
            setting_value = getattr(config, setting)
        settings_dict[setting] = setting_value

    return settings_dict


def set_dot_env(settings: dict[str, str], dotenv_path: str = ".env") -> None:
    """
    Set the environment variables to the .env file

    Args:
        settings (dict[str, str]): Dictionary containing settings and their values
        dotenv_path (str): .env file
    """
    current_settings = dotenv_values(dotenv_path)

    for setting, value in settings.items():
        # Check if the setting already exists in the .env file and not CSRF token
        if (
            (setting not in current_settings or current_settings[setting] != value)
            and setting != "SUBMIT"
            and setting != "CSRF_TOKEN"
        ):
            set_key(dotenv_path, setting, str(value))
