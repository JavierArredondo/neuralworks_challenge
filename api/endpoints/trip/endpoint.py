import pandas as pd
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotAcceptable, NotFound

from .parser import trip_parser
from .trip import Trip

endpoint = Namespace("trip", description="Queries for trips")

parser = trip_parser()


@endpoint.route("/bounding_box")
@endpoint.param("long_max", "Longitude for geospatial query", type=float)
@endpoint.param("lat_max", "Latitude for geospatial query", type=float)
@endpoint.param("long_min", "Longitude for geospatial query", type=float)
@endpoint.param("lat_min", "Latitude for geospatial query", type=float)
@endpoint.param("region", "Name of the region", type=str)
@endpoint.response(200, "Success")
@endpoint.response(404, "Trip not found")
class BoundingBox(Resource):
    @endpoint.expect(trip_parser)
    def get(self):
        args = parser.parse_args()
        for k, v in args.items():
            if v is None:
                raise NotAcceptable(f"Miss '{k}' key in requests")
        bounding_box = Trip.bounding_box(args)
        if len(bounding_box):
            df = pd.DataFrame(bounding_box, columns=["week", "weekly_trips"])
            mean_weekly_trips = df["weekly_trips"].mean()
            return {"mean_weekly_trips": mean_weekly_trips}
        raise NotFound("Trips not found")
