"""
Forms for the flask app
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


# Ignoring type b/c flask_wtf does not have stubs
class EnvVariableForm(FlaskForm):  # type: ignore[misc]
    """
    Form for environment variables
    """

    latitude = StringField("Latitude", validators=[InputRequired()])
    longitude = StringField("Longitude", validators=[InputRequired()])
    weather_api_token = StringField("Weather API Token", validators=[InputRequired()])
    train_api_token = StringField("Train API Token", validators=[InputRequired()])
    submit = SubmitField("Update")
