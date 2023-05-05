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


@app_views.route("/states")
def get_all_states():
    """Gets a lists of all states object
    """
    states = storage.all(State).values()
    states_list = list(map(lambda state: state.to_dict(), states))
    response = jsonify(states_list)
    response.status_code = 200
    return response


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """
    Gets a state object from ID
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    response = jsonify(state.to_dict())
    response.status_code = 200
    return response


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a state object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()

    if "name" not in data.keys():
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    response = jsonify(state.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Updates a state object
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()

    for key, value in data.items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(state, key, value)
    state.save()
    response = jsonify(state.to_dict())
    response.status_code = 200
    return response
