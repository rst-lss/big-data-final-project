# `data-ingestor.py`

This Python script downloads the Adult dataset from the UCI Machine Learning Repository and writes each row as a message into a Kafka broker. The script is designed to simulate a continuous stream of data by sending rows from the dataset to a Kafka topic at a specified interval. The data is preprocessed and encoded before being sent, making it ready for downstream processing or machine learning tasks.


### Constants

```python
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-0.kafka-headless:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "adult-stream")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL", 0.1))
```

**Explanation:**
- `KAFKA_BROKER`: The address of the Kafka broker. This can be set via an environment variable, but it defaults to `kafka-0.kafka-headless:9092` if not provided.
- `KAFKA_TOPIC`: The Kafka topic where the data will be sent. This can also be set via an environment variable, with a default value of `adult-stream`.
- `SEND_INTERVAL`: The time interval (in seconds) between sending each row of data to Kafka. This can be configured via an environment variable, with a default value of `0.1` seconds.


### Download Function

```python
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
```

**Explanation:**
- This function downloads the Adult dataset from the UCI Machine Learning Repository if it doesn't already exist locally.
- The dataset is saved as `adult.data` in the current working directory.
- If the file already exists, the function simply prints a message indicating that the dataset is already downloaded.

### Create Kafka Client

```python
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)
```

**Explanation:**
- This code initializes a Kafka producer client using the `KafkaProducer` class from the `kafka-python` library.
- The `bootstrap_servers` parameter specifies the Kafka broker address.
- The `value_serializer` parameter is a function that serializes the data (in this case, converting it to a JSON string and then encoding it as UTF-8) before sending it to Kafka.

### Load Dataset

```python
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
```

**Explanation:**
- The `download_dataset()` function is called to ensure the dataset is available locally.
- The dataset is then loaded into a Pandas DataFrame using `pd.read_csv()`.
- Since the dataset doesn't have a header row, the `header=None` parameter is used, and column names are explicitly provided using the `names` parameter.


### Small Preprocess

```python
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
```

**Explanation:**
- The dataset contains missing values represented by `" ?"`. These are replaced with `pd.NA` (Pandas' representation of missing values).
- Rows with missing values are dropped using `df.dropna()`.
- The `income` column is converted from a string (e.g., `" <=50K"`, `" >50K"`) to a binary integer (0 or 1) using the `map()` function.
- Categorical columns (e.g., `workclass`, `education`, etc.) are encoded into numerical values using `LabelEncoder`. This is necessary because many machine learning models require numerical input.
- The `encoders` dictionary stores the `LabelEncoder` instances for each categorical column, which could be useful for decoding the values later.


### Send to Kafka

```python
while True:
    for _, row in df.iterrows():
        data = row.to_dict()
        producer.send(KAFKA_TOPIC, value=data)
        time.sleep(SEND_INTERVAL)

    producer.flush()
```

**Explanation:**
- The script enters an infinite loop (`while True`) to continuously send data to Kafka.
- For each row in the DataFrame, the row is converted to a dictionary using `row.to_dict()`.
- The dictionary is sent to the Kafka topic specified by `KAFKA_TOPIC` using the `producer.send()` method.
- The `time.sleep(SEND_INTERVAL)` function introduces a delay between sending each row, as specified by the `SEND_INTERVAL` constant.
- After sending all rows, `producer.flush()` ensures that all messages are sent to Kafka before the loop restarts.
