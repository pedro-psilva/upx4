#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from app import app, init_database

# Initialize database
init_database()

if __name__ == "__main__":
    app.run()
