#!/usr/bin/python3
"""
A script that defines an endpoint
that returns the status of the API
"""


if __name__ == '__main__':
    from flask import Flask, jsonify
    from models import storage
    from api.v1.views import app_views
    from flask_cors import CORS
    from os import getenv

    app = Flask(__name__)
    app.register_blueprint(app_views)
    resources = {
        "/*": {
            "origins": "0.0.0.0",
        }
    }
    CORS(app, resources=resources)

    @app.teardown_appcontext
    def handleTearDown(exception):
        """
        A method to handle app tear down context
        it closes the storage session
        """
        storage.close()

    @app.errorhandler(404)
    def not_found_error(e):
        """
        error handler for 404 error
        """
        data = {"error": "Not found"}
        response = jsonify(data)
        response.status_code = 404
        return response

    @app.errorhandler(400)
    def handle_400_error(e):
        """
        error handler for 400 error
        """
        return e.description, 400

    app.run(getenv('HBNB_API_HOST') or "0.0.0.0",
            port=getenv('HBNB_API_PORT' or 5000),
            threaded=True)
