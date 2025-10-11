#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from a2wsgi import ASGIMiddleware
from main import app, initialize_app

# Initialize the application (database, etc.)
initialize_app()

# FastAPI (ASGI) to WSGI adapter for Passenger
application = ASGIMiddleware(app)
