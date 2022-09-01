import os

from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, Index, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String)
    origin_coord = Column(Geometry(geometry_type="POINT"))
    destination_coord = Column(Geometry(geometry_type="POINT"))
    datetime = Column(DateTime)
    datasource = Column(String)
    group = Column(Integer)


if __name__ == "__main__":
    username = os.getenv("USER", "an_user")
    password = os.getenv("PASSWORD", "a_password")
    database = os.getenv("DB", "neuralworks")
    host = os.getenv("HOST", "localhost")

    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:5432/{database}", echo=False
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    Trip.__table__.create(engine)

    trip_region_index = Index("idx_region", Trip.region, postgresql_using="btree")
    trip_region_index.create(bind=engine)

    trip_datetime_index = Index("idx_datetime", Trip.datetime, postgresql_using="btree")
    trip_datetime_index.create(bind=engine)
