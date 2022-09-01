from flask_restx import reqparse


def trip_parser():
    trip = reqparse.RequestParser()

    trip.add_argument(
        "lat_min", type=float, dest="lat_min", location="args", help="Minimum latitude"
    )

    trip.add_argument(
        "long_min",
        type=float,
        dest="long_min",
        location="args",
        help="Minimum longitude",
    )

    trip.add_argument(
        "lat_max", type=float, dest="lat_max", location="args", help="Maximum latitude"
    )

    trip.add_argument(
        "long_max",
        type=float,
        dest="long_max",
        location="args",
        help="Maximum longitude",
    )

    trip.add_argument(
        "region", type=str, dest="region", location="args", help="Name of the region"
    )

    return trip
