#!/usr/bin/python3

"""
Creates the status route
"""

from api.v1.views import app_views
from flask import jsonify
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage


@app_views.route('/status')
def status():
    """
    returns a json with status set to OK
    """
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route('/stats')
def stats():
    """
    Retrieves the number of each objects
    by type
    """
    states = storage.count(State)
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    users = storage.count(User)

    stat = {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "states": states,
        "users": users,
        "reviews": reviews
    }
    response = jsonify(stat)
    response.status_code = 200
    return response
