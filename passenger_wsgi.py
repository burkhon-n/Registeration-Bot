#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from a2wsgi import ASGIMiddleware, WSGIMiddleware
from main import app

# FastAPI to WSGI
application = WSGIMiddleware(app)
