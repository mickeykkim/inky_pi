"""
Routes for flask app
"""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for
from werkzeug import Response

from inky_web.forms import ConfigurationForm
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
    settings = get_dot_env()
    return render_template("display_configs.html", settings=settings)


@edit_configs_bp.route("/edit", methods=["GET", "POST"])  # type: ignore[misc]
def edit() -> Response | str:
    """
    Edit configuration settings page

    Returns:
        Response: Redirect to same page
        str: Edit configuration settings page
    """
    form = ConfigurationForm()

    if form.validate_on_submit():
        new_settings = {field.name.upper(): field.data for field in form}
        set_dot_env(new_settings)
        return redirect(url_for("display_configs.display"))

    current_settings = get_dot_env()
    for field in form:
        field_id = field.name.upper()
        if field_id in current_settings:
            field.data = current_settings[field_id]

    return render_template("edit_configs.html", form=form)
