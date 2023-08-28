"""
This is the Flask frontend for the application. It is responsible for changing
configuration, environment variables, and running the application.

Usage:
    python run.py
"""
import sys

from flask_app.app import main

if __name__ == "__main__":
    main(sys.argv[1:])
