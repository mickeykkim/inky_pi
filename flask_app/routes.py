"""
Routes for flask app
"""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for
from werkzeug import Response

from flask_app.forms import EnvVariableForm
from flask_app.util import get_dot_env, set_dot_env

main_bp = Blueprint("main", __name__)
display_env_bp = Blueprint("display_env", __name__)
edit_env_bp = Blueprint("edit_env", __name__)


@main_bp.route("/")
def index() -> str:
    """
    Index route

    Returns:
        str: Index page
    """
    return render_template("index.html")


@display_env_bp.route("/display")
def display() -> str:
    """
    Display environment variables

    Returns:
        str: Display environment variables page
    """
    latitude, longitude, weather_api_token, train_api_token = get_dot_env()

    return render_template(
        "display_env.html",
        latitude=latitude,
        longitude=longitude,
        weather_api_token=weather_api_token,
        train_api_token=train_api_token,
    )


@edit_env_bp.route("/edit_env", methods=["GET", "POST"])
def edit_env() -> Response | str:
    """
    Edit environment variables

    Returns:
        Response: Redirect to same page
        str: Edit environment variables page
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
        return redirect(url_for("display_env.display"))

    latitude, longitude, weather_api_token, train_api_token = get_dot_env()

    # Populate the form fields with current environment variables
    form.latitude.data = latitude
    form.longitude.data = longitude
    form.weather_api_token.data = weather_api_token
    form.train_api_token.data = train_api_token

    return render_template("edit_env.html", form=form)
