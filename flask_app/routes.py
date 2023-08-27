"""
Routes for flask app
"""

from flask import Response, request

from flask_app import app

TESTING_MESSAGE = "Response Test instance of mocked panelapp..."


@app.route("/panelapp", methods=["GET", "HEAD"])
@app.route("/panelapp/", methods=["GET", "HEAD"])
def panelapp() -> Response | str:
    """
    Flask App homepage handling.

    Returns:
         Response | str: The response object or a string (if encountering a GET request)
    """
    if request.method == "HEAD":
        return Response("ok", status=302, mimetype="application/json")
    else:
        return TESTING_MESSAGE
