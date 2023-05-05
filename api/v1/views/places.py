#!/usr/bin/python3
"""This file contains the Flask API Place module"""

import json
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """function to list cities by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = storage.all(Place).values()
    places_with_city_id = list(filter(lambda place: place.city_id == city_id,
                               all_places))
    place_list = list(map(lambda place: place.to_dict(),
                          places_with_city_id))
    response = jsonify(place_list)
    response.status_code = 200
    return response


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """function to get place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """function deletes place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_obj_place(city_id):
    """function creates new instance """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        abort(400, "Missing name")
    obj = Place(**data)
    obj.city_id = city_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def post_place(place_id):
    """ update place by id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places_by_id():
    """function to search places by id """
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    states = data.get("states", None)
    cities = data.get("cities", None)
    amenities = data.get("amenities", None)

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        all_places = storage.all(Place).values()
        for state in states_obj:
            cities_in_state = state.cities
            for city in cities_in_state:
                for p in all_places:
                    if p.city_id == city.id:
                        list_places.append(p)

    if cities:
        all_places = storage.all(Place).values()
        for c_id in cities:
            for p in all_places:
                if p.city_id == c_id:
                    if p not in list_places:
                        list_places.append(p)

    if amenities:
        filtered_list = []
        if len(list_places) == 0:
            list_places = storage.all(Place).values()

        if storage_t == 'db':
            amenity_objs = []
            for amenity in amenities:
                amenity_objs.append(storage.get(Amenity, amenity))
            for place in list_places:
                if all(amen_obj in place.amenities
                        for amen_obj in amenity_objs):
                    filtered_list.append(place)
        else:
            for place in list_places:
                if all(ids in place.amenity_ids for ids in amenities):
                    filtered_list.append(place)
        list_places = filtered_list

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop("amenities", None)
        d.pop("amenity_ids", None)
        places.append(d)

    return jsonify(places)
