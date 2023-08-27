#!/usr/bin/env python
"""

Usage:
    >>> python run.py
"""

from flask_app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
