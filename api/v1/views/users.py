#!/usr/bin/python3
"""
Creates a new view for USER objects
that handles all default RESTFul API actions
"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import request, abort, jsonify


@app_views.route("/users", strict_slashes=False)
def users():
    """
    gets a list of all the users
    """
    users = storage.all(User).values()
    users_list = list(map(lambda user: user.to_dict(), users))
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user(user_id):
    """
    gets a single singe user
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        user_dict = user.to_dict()
        return jsonify(user_dict), 200


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user from database
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        response = jsonify({})
        response.status_code = 200
        return response


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def add_user():
    """
    Add a new user
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    else:
        data = request.get_json()
        if "email" not in data.keys():
            abort(400, "Missing email")
        if "password" not in data.keys():
            abort(400, "Missing password")
        user = User(**data)
        user.save()
        response = jsonify(user.to_dict())
        response.status_code = 201
        return response


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing user details
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        if not request.is_json:
            abort(400, "Not a JSON")
        else:
            data = request.get_json()
            for key in data.keys():
                if key in ["id", "email", "created_at", "updated_at"]:
                    pass
                else:
                    setattr(user, key, data[key])
            user.save()
            response = jsonify(user.to_dict())
            response.status_code = 200
            return response
