from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry, text

db = SQLAlchemy()


class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region = db.Column(db.String)
    origin_coord = db.Column(Geometry(geometry_type="POINT"))
    destination_coord = db.Column(Geometry(geometry_type="POINT"))
    datetime = db.Column(db.DateTime)
    datasource = db.Column(db.String)
    group = db.Column(db.Integer)

    @classmethod
    def bounding_box(cls, args: dict):
        complex_query = """select date_part('week', datetime) as week, count(*) as weekly_trip
        from trips
        where region=:region and origin_coord && st_makeenvelope(:lat_min, :long_min, :lat_max, :long_max)
        group by week
        """
        sql_statement = text(complex_query)
        response = db.engine.execute(sql_statement, args)
        response = [r for r in response]
        return response
