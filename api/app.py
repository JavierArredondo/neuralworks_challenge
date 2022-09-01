from db import db
from endpoints.ingestion.endpoint import endpoint as ingestion_endpoint
from endpoints.trip.endpoint import endpoint as trip_endpoint
from flask import Flask
from flask_restx import Api


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    api = Api(app, title="NeuralWorks Challenge")

    api.add_namespace(trip_endpoint, path="/trip")
    api.add_namespace(ingestion_endpoint, path="/ingestion")

    return app


if __name__ == "__main__":
    app_service = create_app("settings")
    app_service.run(debug=True)
