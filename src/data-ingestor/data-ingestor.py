import json
import os
import time
import urllib.request

import numpy as np
import pandas as pd
from kafka import KafkaProducer
from sklearn.preprocessing import LabelEncoder, StandardScaler

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-0.kafka-headless:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "adult-income-stream")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL", 0.5))


def load_adult_income_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    column_names = [
        "age",
        "workclass",
        "fnlwgt",
        "education",
        "education-num",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
        "native-country",
        "income",
    ]

    urllib.request.urlretrieve(url, "adult.data")
    df = pd.read_csv("adult.data", header=None, names=column_names)

    df = df.replace(" ?", np.nan).dropna()

    numeric_cols = [
        "age",
        "fnlwgt",
        "education-num",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
    ]

    categorical_cols = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]
    label_encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    target_encoder = LabelEncoder()
    df["income"] = target_encoder.fit_transform(df["income"])

    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df, numeric_cols + categorical_cols, "income"


def send_to_kafka(data, bootstrap_servers=KAFKA_BROKER, topic=KAFKA_TOPIC):
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    df, feature_cols, target_col = data

    for _, row in df.iterrows():
        record = {"features": row[feature_cols].tolist(), "label": int(row[target_col])}

        producer.send(topic, record)
        print(f"Sent record: {record}")

        time.sleep(SEND_INTERVAL)

    producer.flush()
    producer.close()


if __name__ == "__main__":
    dataset = load_adult_income_data()
    send_to_kafka(dataset)
