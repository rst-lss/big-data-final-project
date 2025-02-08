from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import IntegerType, StructField, StructType

spark = SparkSession.builder.appName("EnsembleModel").getOrCreate()

schema = StructType(
    [
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
    ]
)

feature_cols = [
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
]


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
        col("age"),
        col("education"),
        col("occupation"),
        col("income").alias("actual_income"),
        col("prediction").alias("predicted_income"),
        col("probability"),
    )

    query = output.writeStream.outputMode("append").format("console").start()

    return query


def main():
    print("Training initial model...")
    model = train_model()

    print("Starting streaming predictions...")
    query = process_stream(model)

    query.awaitTermination()


if __name__ == "__main__":
    main()
