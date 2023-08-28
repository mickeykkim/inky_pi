"""
This is the main module of the Flask app. It creates the Flask app object and
imports the routes module.
"""
from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv
from flask import Flask

from flask_app.routes import display_env_bp, edit_env_bp, main_bp


# pylint: disable=C0103
class AppConfig:
    """
    Configuration object class
    """

    DEBUG: bool
    TESTING: bool
    SECRET_KEY: str


def create_app(config: AppConfig | None = None) -> Flask:
    """
    Create the Flask app

    Args:
        config (AppConfig): Configuration object

    Returns:
        Flask: Flask app object
    """
    app = Flask(__name__)

    if config:
        app.config.from_object(config)
    else:
        load_dotenv()
        app_config = AppConfig()
        app_config.DEBUG = bool(os.getenv("FLASK_DEBUG"))
        app_config.TESTING = bool(os.getenv("FLASK_TESTING"))
        app_config.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "")
        app.config.from_object(app_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(display_env_bp)
    app.register_blueprint(edit_env_bp)

    return app


def parse_args(cl_arguments: list[str]) -> argparse.Namespace:
    """
    Parse command line arguments

    Args:
        cl_arguments (list[str]): Command line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Flask App for configuring and running Inky Pi"
    )
    parser.add_argument("--host", default="localhost", help="Host to run the server on")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run the server on"
    )
    return parser.parse_args(cl_arguments)


def main(cl_arguments: list[str]) -> None:
    """
    Main function

    Args:
        cl_arguments (list[str]): Command line arguments

    Returns:
        None
    """
    args = parse_args(cl_arguments)
    flask_app = create_app()
    flask_app.run(host=args.host, port=args.port)
