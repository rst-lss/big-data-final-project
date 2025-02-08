import json
import os
import time

import pandas as pd
import requests
from kafka import KafkaProducer
from sklearn.preprocessing import LabelEncoder


def download_dataset():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    if not os.path.exists("adult.data"):
        print("Downloading dataset...")
        response = requests.get(url)
        with open("adult.data", "wb") as f:
            f.write(response.content)
        print("Dataset downloaded successfully")
    else:
        print("Dataset already exists")


producer = KafkaProducer(
    bootstrap_servers=["kafka-0.kafka-headless:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

download_dataset()

df = pd.read_csv(
    "adult.data",
    header=None,
    names=[
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
    ],
)

df = df.replace(" ?", pd.NA)
df = df.dropna()
df["income"] = df["income"].map({" <=50K": 0, " >50K": 1})

categorical_columns = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]
encoders = {}
for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    encoders[column] = le

topic = "adult-stream"
while True:
    for _, row in df.iterrows():
        data = row.to_dict()
        producer.send(topic, value=data)
        time.sleep(0.5)

    producer.flush()
