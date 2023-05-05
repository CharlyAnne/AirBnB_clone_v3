#!/usr/bin/python3

"""
Creates a new view for Review objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from flask import request, abort, jsonify
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews_of_place(place_id):
    """
    Retrieves the lists of all Review object
    of a place
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    else:
        reviews = place.reviews
        reviews_list = list(map(lambda review: review.to_dict(), reviews))
        response = jsonify(reviews_list)
        return response


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a single Review object
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    else:
        response = jsonify(review.to_dict())
        response.status_code = 200
        return response


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a review based on the review id
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        response = jsonify({})
        response.status_code = 200
        return response


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def adds_review(place_id):
    """
    Creates a review for a place
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    else:
        if not request.is_json:
            abort(400, "Not a JSON")
        else:
            data = request.get_json()
            if "user_id" not in data.keys():
                abort(400, "Missing user_id")
            user = storage.get(User, data["user_id"])

            if user is None:
                abort(404)
            if "text" not in data.keys():
                abort(400, "Missing text")
            review = Review(**data)
            review.place_id = place_id
            review.save()

            response = jsonify(review.to_dict())
            response.status_code = 201
            return response


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    updates a review
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    else:
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        for key, value in data.items():
            if key in ["id",
                       "user_id",
                       "place_id",
                       "created_at",
                       "updated_at"]:
                pass
            else:
                setattr(review, key, value)
        review.save()
        response = jsonify(review.to_dict())
        response.status_code = 200
        return response
