# `ensemble-model.py`

This PySpark job is designed to process streaming data from Kafka for real-time machine learning predictions. The application reads historical data to train a Random Forest model and then uses this model to make predictions on incoming streaming data.

The application performs two main functions:
1. Training an ensemble model using historical data from Kafka
2. Making real-time predictions on incoming data streams

### Usage

To run this application, ensure you have:
1. A running Kafka cluster with the specified broker address
2. The "adult-stream" topic created and containing data in the expected format
3. PySpark environment with necessary dependencies installed

The application will continuously process incoming data and output predictions to the console.

### Spark Session Setup

```python
spark = SparkSession.builder.appName("EnsembleModel").getOrCreate()
```

This code initializes a Spark session with the application name "EnsembleModel". The `getOrCreate()` method either creates a new session or returns an existing one, ensuring we don't create multiple sessions unnecessarily.

### Data Structure Definition

```python
schema = StructType([
    StructField("age", IntegerType(), True),
    StructField("workclass", IntegerType(), True),
    StructField("fnlwgt", IntegerType(), True),
    StructField("education", IntegerType(), True),
    StructField("education-num", IntegerType(), True),
    StructField("marital-status", IntegerType(), True),
    StructField("occupation", IntegerType(), True),
    StructField("relationship", IntegerType(), True),
    StructField("race", IntegerType(), True),
    StructField("sex", IntegerType(), True),
    StructField("capital-gain", IntegerType(), True),
    StructField("capital-loss", IntegerType(), True),
    StructField("hours-per-week", IntegerType(), True),
    StructField("native-country", IntegerType(), True),
    StructField("income", IntegerType(), True),
])

feature_cols = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country"
]
```

This section defines:
- A schema for the input data using Spark's `StructType` and `StructField`
- All fields are defined as integers with nullable=True
- The `feature_cols` list specifies which columns will be used as features for the model
- The "income" field serves as the target variable for prediction

### Model Training

```python
def train_model():
    df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
        .option("subscribe", "adult-stream")
        .option("startingOffsets", "earliest")
        .option("endingOffsets", "latest")
        .load()
    )

    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

    rf = RandomForestClassifier(
        labelCol="income", featuresCol="features", numTrees=100, maxDepth=10, seed=42
    )

    pipeline = Pipeline(stages=[assembler, rf])
    model = pipeline.fit(parsed_df)

    model.write().overwrite().save("/tmp/adult_income_model")
    return model
```

The `train_model()` function:
1. Reads historical data from Kafka using specified configurations
   - Connects to Kafka broker at "kafka-0.kafka-headless:9092"
   - Subscribes to "adult-stream" topic
   - Reads all available data from earliest to latest offset
2. Parses the JSON data according to the defined schema
3. Creates a feature vector using `VectorAssembler`
4. Initializes a Random Forest classifier with:
   - 100 trees
   - Maximum depth of 10
   - Fixed random seed for reproducibility
5. Creates and fits a pipeline that combines feature assembly and model training
6. Saves the trained model to disk and returns it


### Stream Processing

```python
def process_stream(model):
    streaming_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
        .option("subscribe", "adult-stream")
        .load()
    )

    parsed_stream = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    predictions = model.transform(parsed_stream)

    output = predictions.select(
        col("age"), col("education"), col("occupation"),
        col("income").alias("actual_income"),
        col("prediction").alias("predicted_income"),
        col("probability")
    )

    query = output.writeStream.outputMode("append").format("console").start()

    return query
```

The `process_stream()` function:
1. Sets up a streaming connection to Kafka using the same broker and topic
2. Parses incoming JSON data using the same schema
3. Applies the trained model to make predictions on the streaming data
4. Selects relevant columns for output, including:
   - Key features: age, education, occupation
   - Actual income value
   - Predicted income value
   - Prediction probabilities
5. Configures the output stream to:
   - Use "append" mode (only new records are output)
   - Write results to console
   - Start the streaming query

### Application Entry Point

```python
def main():
    print("Training initial model...")
    model = train_model()

    print("Starting streaming predictions...")
    query = process_stream(model)

    query.awaitTermination()

if __name__ == "__main__":
    main()
```

The main function orchestrates the application flow:
1. Trains the initial model using historical data
2. Initiates the streaming process using the trained model
3. Waits for the streaming query to terminate
4. Uses the `if __name__ == "__main__":` idiom to ensure the code only runs when executed directly

