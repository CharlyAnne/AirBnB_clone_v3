#!/usr/bin/python3

"""
Creates a new view for city objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import request, abort, jsonify


@app_views.route("/states/<state_id>/cities")
def cities_of_state(state_id):
    """
    retrieves the list of all City object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        cities = state.cities
        cities_list = []
        for city in cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)


@app_views.route('/cities/<city_id>')
def city(city_id):
    """
    retrieved a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city_dict = city.to_dict()
        return jsonify(city_dict)


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        response = jsonify({})
        response.status_code = 200
        return response


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city_to_state(state_id):
    """
    Adds a city to a state instance
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    else:
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if "name" not in data.keys():
            abort(400, "Missing name")
        else:
            data["state_id"] = state_id
            city = City(**data)
            city.save()
            city_dict = city.to_dict()
            response = jsonify(city_dict)
            response.status_code = 201
            return response


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a city instance
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    else:
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        for key in data.keys():
            if key in ["id", "state_id", "created_at", "updated_at"]:
                pass
            else:
                setattr(city, key, data[key])
        city.save()
        city_dict = city.to_dict()
        response = jsonify(city_dict)
        response.status_code = 200
        return response
