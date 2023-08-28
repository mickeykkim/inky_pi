"""
This is the main module of the Flask app. It creates the Flask app object and
imports the routes module.
"""
from __future__ import annotations

from typing import Any

from flask import Flask

from flask_app.routes import config_bp, main_bp


def create_app(config: Any | None = None) -> Flask:
    """
    Create the Flask app

    Args:
        config:

    Returns:
        Flask: Flask app object
    """
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    app.register_blueprint(main_bp)
    app.register_blueprint(config_bp)

    return app
