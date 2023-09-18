"""
Routes for flask app
"""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for
from werkzeug import Response

from inky_web.forms import EnvVariableForm
from inky_web.util import get_dot_env, set_dot_env

main_bp = Blueprint("main", __name__)
display_configs_bp = Blueprint("display_configs", __name__)
edit_configs_bp = Blueprint("edit_configs", __name__)


@main_bp.route("/")  # type: ignore[misc]
def index() -> str:
    """
    Index route

    Returns:
        str: Index page
    """
    return render_template("index.html")


@display_configs_bp.route("/display")  # type: ignore[misc]
def display() -> str:
    """
    Display configuration settings page

    Returns:
        str: Display configuration settings page
    """
    latitude, longitude, weather_api_token, train_api_token = get_dot_env()

    return render_template(
        "display_configs.html",
        latitude=latitude,
        longitude=longitude,
        weather_api_token=weather_api_token,
        train_api_token=train_api_token,
    )


@edit_configs_bp.route("/edit", methods=["GET", "POST"])  # type: ignore[misc]
def edit() -> Response | str:
    """
    Edit configuration settings page

    Returns:
        Response: Redirect to same page
        str: Edit configuration settings page
    """

    form = EnvVariableForm()

    if form.validate_on_submit():
        # Update the values based on the form data
        latitude = form.latitude.data
        longitude = form.longitude.data
        weather_api_token = form.weather_api_token.data
        train_api_token = form.train_api_token.data

        # Update the .env file with the new values
        set_dot_env(
            latitude=latitude,
            longitude=longitude,
            weather_api_token=weather_api_token,
            train_api_token=train_api_token,
        )

        # Redirect to display page
        return redirect(url_for("display_configs.display"))

    latitude, longitude, weather_api_token, train_api_token = get_dot_env()

    # Populate the form fields with current configuration settings
    form.latitude.data = latitude
    form.longitude.data = longitude
    form.weather_api_token.data = weather_api_token
    form.train_api_token.data = train_api_token

    return render_template("edit_configs.html", form=form)
