#!/usr/bin/env python3
"""
This module sets up the Flask Blueprint for the app views.

The Blueprint defines the routes and views related to the API.
It sets the URL prefix for the routes to "/api/v1".

The module imports the necessary view functions from
other modules and initializes the app.

Modules included:
- `index`: Defines routes and views for the root or index of the API.
- `users`: Defines routes and views for user-related actions.
"""

from flask import Blueprint

# Create a new Blueprint for the app views with URL prefix "/api/v1"
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import route functions from different view modules
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

"""
Load user data from file, assuming this method loads data into the User model
"""
User.load_from_file()
