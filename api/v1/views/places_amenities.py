#!/usr/bin/python3

"""
A new view for Place amenity
"""
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/amenities',
                 methods=["GET"], strict_slashes=False)
def get_amenities(place_id):
    """
    Gets a list of all amenities based on the
    place id
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if storage_t == "db":
        amenities = place.amenities
        amenities_list = list(map(lambda amenity: amenity.to_dict(),
                                  amenities))
        return jsonify(amenities_list)
    amenities = list(map(lambda amenity_id: storage.get(Amenity,
                                                        amenity_id).to_dict(),
                         place.amenity_ids))
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_amenity_from_place(place_id, amenity_id):
    """
    Deletes an Amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
    storage.delete(amenity)
    if storage_t != "db":
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    links and Amenity object to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.add(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
