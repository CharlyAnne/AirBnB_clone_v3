#!/usr/bin/python3
"""
intializes the views blueprint
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from . import index
from . import cities
from . import places_reviews
from . import users
from . import amenities
from . import states
from . import places
from . import places_amenities
