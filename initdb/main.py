import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

Base = declarative_base()


class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String)
    origin_coord = Column(Geometry(geometry_type='POINT'))
    destination_coord = Column(Geometry(geometry_type='POINT'))
    datetime = Column(DateTime)
    datasource = Column(String)
    group = Column(Integer)


if __name__ == "__main__":
    username = os.getenv("USER", "an_user")
    password = os.getenv("PASSWORD", "a_password")
    database = os.getenv("DB", "neuralworks")
    host = os.getenv("HOST", "localhost")

    engine = create_engine(f'postgresql://{username}:{password}@{host}:5432/{database}', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Trip.__table__.create(engine)
