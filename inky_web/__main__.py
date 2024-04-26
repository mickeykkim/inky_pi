"""
This is the Flask frontend for the application. It is responsible for changing
configuration, environment variables, and running the application.

Usage:
    python -m inky_web
"""

from __future__ import annotations

import argparse
import os
import sys
import webbrowser

from dotenv import load_dotenv
from flask import Flask

from inky_web.routes import display_configs_bp, edit_configs_bp, main_bp


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
        app_config.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-me")
        app.config.from_object(app_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(display_configs_bp)
    app.register_blueprint(edit_configs_bp)

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
    parser.add_argument(
        "--no-launch",
        action="store_true",
        help="Don't launch web page in external browser",
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
    if not args.no_launch:
        webbrowser.open(f"http://{args.host}:{args.port}")
    flask_app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main(sys.argv[1:])
