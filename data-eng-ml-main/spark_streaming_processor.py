# spark_streaming_app.py (Final Production Version)
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, lit
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
import joblib
import pandas as pd # ใช้ Pandas ใน UDF เพื่อจัดการ One-Hot Encoding
import time
import sys

# --- Configuration ---
MODEL_PATH = "/home/jovyan/work/model/anomaly_model.joblib"
FEATURES_PATH = "/home/jovyan/work/model/model_features.txt"
KAFKA_BOOTSTRAP_SERVERS = "kafka_fraud:9093"
KAFKA_TOPIC = "transactions" 
POSTGRES_URL = "jdbc:postgresql://postgres_fraud_db:5432/ecomm_fraud_db"
POSTGRES_PROPERTIES = {
    "user": "postgres",
    "password": "123",
    "driver": "org.postgresql.Driver"
}
TRANSACTIONS_TABLE = "transactions"
ANOMALIES_TABLE = "anomalies"

# --- Load Model, Features, and Define UDF ---
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
    
    with open(FEATURES_PATH, 'r') as f:
        MODEL_FEATURES = [line.strip() for line in f.readlines()]
    print(f"Model features loaded: {MODEL_FEATURES}")
    
except FileNotFoundError as e:
    # หากไฟล์โมเดลหาย จะ log error แล้วออกจากโปรแกรม
    print(f"🚨 FATAL ERROR: Missing file: {e.filename}. System exit.")
    sys.exit(1)

def predict_anomaly(amount, product_category):
    """
    UDF to predict anomaly using the loaded model and One-Hot Encoding logic.
    """
    if not MODEL_FEATURES:
        return 0 # ถ้าโหลดฟีเจอร์ไม่ได้ ให้ถือว่าปกติไว้ก่อน (Fallback)

    try:
        # 1. สร้าง DataFrame จาก input
        data = {'amount': [float(amount)], 'product_category': [product_category]}
        df = pd.DataFrame(data)
    except ValueError:
        return 1 # 1 = Anomaly หากค่า amount แปลงไม่ได้
        
    # 2. ทำ One-Hot Encoding (ต้องใช้ drop_first=True เหมือนตอน train)
    df_encoded = pd.get_dummies(df, columns=['product_category'], drop_first=True)
    
    # 3. จัดเรียงคอลัมน์ให้ตรงกับตอน train
    df_final = pd.DataFrame(0.0, index=[0], columns=MODEL_FEATURES)
    
    for col_name in df_encoded.columns:
        if col_name in MODEL_FEATURES:
            df_final.loc[0, col_name] = df_encoded.loc[0, col_name].astype(float)
    
    # 4. ทำนาย: prediction: 1 = normal, -1 = anomaly
    prediction = model.predict(df_final)

    # 5. แปลงค่าผลลัพธ์ให้ตรงกับ DDL (1=ผิดปกติ, 0=ปกติ)
    if int(prediction[0]) == -1:
        return 1  # 1 = ผิดปกติ (Anomaly)
    else:
        return 0  # 0 = ปกติ (Normal)

# ลงทะเบียน UDF
anomaly_udf = udf(predict_anomaly, IntegerType())

# --- Spark Session ---
print("Starting Spark session...")
spark = SparkSession.builder \
    .appName("RealTimeAnomalyDetection") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.5.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")
print("Spark session created.")


# --- Define Schema for Kafka Data ---
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("product_category", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("ip_address", StringType(), True)
])

# --- Read Stream from Kafka ---
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# --- Process Stream ---
transactions_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("transaction_timestamp", col("timestamp").cast(TimestampType())) \
    .drop("timestamp") 

# Apply the anomaly detection model using the UDF
predictions_df = transactions_df.withColumn(
    "is_anomaly", 
    anomaly_udf(col("amount"), col("product_category"))
)
print("Streaming DataFrame with predictions defined.")


# ----------------------------------------------------------------------------------
# --- Write Streams to PostgreSQL (Production) ---
# ----------------------------------------------------------------------------------

def write_to_postgres_transactions(df, epoch_id):
    # *** ธุรกรรมทั้งหมดไปที่ตาราง transactions ***
    try:
        df_to_write = df.select(
            "transaction_id", "user_id", "amount", "product_category", 
            "transaction_timestamp", "ip_address", col("is_anomaly").alias("is_anomalous")
        )
        df_to_write.write \
            .mode("append") \
            .jdbc(url=POSTGRES_URL, table=TRANSACTIONS_TABLE, properties=POSTGRES_PROPERTIES)
    except Exception as e:
        print(f"🚨 ERROR: Cannot write to 'transactions' table (Epoch {epoch_id}): {e}")


query_all_transactions = predictions_df \
    .writeStream \
    .foreachBatch(write_to_postgres_transactions) \
    .outputMode("update") \
    .start()

# ----------------------------------------------------------------------------------

# Filter สำหรับ Anomaly เท่านั้น
anomalies_df = predictions_df.filter(col("is_anomaly") == 1)

def write_to_postgres_anomalies(df, epoch_id):
    # *** เฉพาะ Anomaly ไปที่ตาราง anomalies ***
    try:
        df_to_write = df.select(
            "transaction_id", "user_id", "amount", "transaction_timestamp"
        ).withColumn("anomaly_type", lit("ML Prediction: Isolation Forest"))
        
        df_to_write.write \
            .mode("append") \
            .jdbc(url=POSTGRES_URL, table=ANOMALIES_TABLE, properties=POSTGRES_PROPERTIES)
    except Exception as e:
        print(f"🚨 ERROR: Cannot write to 'anomalies' table (Epoch {epoch_id}): {e}")


query_anomalies = anomalies_df \
    .writeStream \
    .foreachBatch(write_to_postgres_anomalies) \
    .outputMode("update") \
    .start()

print("Streaming queries started. Writing to PostgreSQL: transactions & anomalies.")
spark.streams.awaitAnyTermination()