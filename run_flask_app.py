"""
This is the Flask frontend for the application. It is responsible for changing
configuration, environment variables, and running the application.

Usage:
    python run_flask_app.py
"""

from flask_app import app

if __name__ == "__main__":
    flask_app = app.create_app()
    flask_app.run()
