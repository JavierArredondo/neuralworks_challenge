import json
import logging
import os
import uuid

import pandas as pd
from confluent_kafka import Producer, admin

KAFKA_CONFIG = {"bootstrap.servers": os.getenv("KAFKA_SERVER", "localhost:9092")}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":
    num_messages = int(os.getenv("NUM_MESSAGES", 10000))
    topic = os.getenv("TOPIC_NAME", "trips")
    data_path = os.getenv("DATA_PATH", "../trips.csv")

    data = pd.read_csv(data_path)

    kafka_client = admin.AdminClient(KAFKA_CONFIG)
    new_topic = admin.NewTopic(topic, 1, 1)
    kafka_client.create_topics([new_topic])
    producer = Producer(KAFKA_CONFIG)

    n = 0
    while n < num_messages:
        index_msg = n % len(data)
        logging.info(f"Producing message {n} with index {index_msg}")
        msg = data.loc[index_msg].to_dict()
        msg = json.dumps(msg).encode("utf-8")
        producer.produce(topic, msg)
        producer.poll(1)
        n += 1
