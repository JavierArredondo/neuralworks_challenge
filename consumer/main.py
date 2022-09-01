import json
import logging
import os
import pickle

import geopandas as gpd
import pandas as pd
from confluent_kafka import Consumer
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

KAFKA_CONFIG = {
    "bootstrap.servers": os.getenv("KAFKA_SERVER", "localhost:9092"),
    "auto.offset.reset": "earliest",
}


def parse_input(df: pd.DataFrame) -> pd.DataFrame:
    df["origin_coord"] = gpd.GeoSeries.from_wkt(df["origin_coord"])
    df["destination_coord"] = gpd.GeoSeries.from_wkt(df["destination_coord"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def preprocess(df: pd.DataFrame, transformer: StandardScaler) -> pd.DataFrame:
    df = parse_input(df)
    features = pd.DataFrame(
        {
            "num_hour": df["datetime"].apply(lambda x: int(x.strftime("%H"))),
            "x_orig": df["origin_coord"].apply(lambda x: x.x),
            "y_orig": df["origin_coord"].apply(lambda x: x.y),
            "x_dest": df["destination_coord"].apply(lambda x: x.x),
            "y_dest": df["destination_coord"].apply(lambda x: x.y),
            "distance": df.apply(
                lambda x: x["origin_coord"].distance(x["destination_coord"]), axis=1
            ),
        }
    )
    p = transformer.transform(features)
    return p


if __name__ == "__main__":
    # Kafka config
    topic = os.getenv("TOPIC_NAME", "trips")
    group_id = os.getenv("GROUP_ID", "test")
    batch_size = os.getenv("BATCH_SIZE", 10)
    # Model config
    model_path = os.getenv("MODEL_PATH", "../models/kmeans.pkl")
    scaler_path = os.getenv("SCALER_PATH", "../models/scaler.pkl")
    # Database config
    username = os.getenv("USER", "an_user")
    password = os.getenv("PASSWORD", "a_password")
    database = os.getenv("DB", "neuralworks")
    host = os.getenv("HOST", "localhost")
    # Init database engine
    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:5432/{database}", echo=False
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(model_path, "rb") as f:
        model = pickle.load(f)
        logging.info("Model loaded successfully")

    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
        logging.info("Scaler loaded successfully")

    KAFKA_CONFIG["group.id"] = group_id
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([topic])
    logging.info(f"Subscribed to {topic}")

    while True:
        msgs = consumer.consume(batch_size)
        if len(msgs):
            logging.info(f"Consumed {len(msgs)} messages")
            data = [json.loads(msg.value()) for msg in msgs]
            data = pd.DataFrame(data)
            preprocessed = preprocess(data.copy(), scaler)
            logging.info("Doing inference")
            groups = model.predict(preprocessed)
            data["group"] = groups
            data.to_sql("trips", engine, if_exists="append", index=False)
            logging.info(f"Stored {len(msgs)} record")
            consumer.commit()
