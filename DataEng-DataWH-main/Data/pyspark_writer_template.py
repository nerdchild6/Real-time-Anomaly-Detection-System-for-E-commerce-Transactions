from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys

# #############################################################################
# 1. การตั้งค่าการเชื่อมต่อ JDBC Parameters
# #############################################################################

# Hostname 'postgres_db' คือชื่อ Service ภายใน Docker Network (สำคัญมาก)
DB_URL = "jdbc:postgresql://postgres_fraud_db:5432/ecomm_fraud_db"

DB_PROPERTIES = {
    "user": "postgres",                     
    "password": "123",                      
    "driver": "org.postgresql.Driver",
}

# #############################################################################
# 2. ฟังก์ชันหลักสำหรับเขียน DataFrame ลงตาราง
# #############################################################################

def write_dataframe_to_postgres(df, table_name, write_mode="append"):
    """
    เขียน PySpark DataFrame ลงในตาราง PostgreSQL ผ่าน JDBC
    """
    row_count = df.count() 
    print(f"--- กำลังเขียนข้อมูล {row_count} แถว ไปยังตาราง {table_name} ด้วยโหมด '{write_mode}' ---")
    
    try:
        df.write \
          .format("jdbc") \
          .option("url", DB_URL) \
          .option("dbtable", table_name) \
          .options(**DB_PROPERTIES) \
          .mode(write_mode) \
          .save()
        print(f"--- เขียนข้อมูลไปยังตาราง {table_name} จำนวน {row_count} แถว สำเร็จ ---")
    except Exception as e:
        print(f"!!! เกิดข้อผิดพลาดในการเขียนข้อมูลไปยัง {table_name}: {e}")
        # Re-raise exception เพื่อให้ Block หลักรับรู้และไปสู่ finally block
        raise e 

# #############################################################################
# 3. Logic การรัน Main (สำหรับทดสอบ End-to-End Ingestion)
# #############################################################################

if __name__ == "__main__":
    
    # 3.1 ตรวจสอบ Arguments (Path ของ CSV)
    if len(sys.argv) < 2:
        print("Usage: spark-submit pyspark_writer_template.py <path_to_csv_file>")
        sys.exit(1)
        
    csv_file_path = sys.argv[1] 
    spark = None # กำหนด spark เป็น None ไว้ก่อน
    
    try:
        # 3.2 สร้าง SparkSession
        spark = SparkSession.builder \
            .appName("EcommFraudWriter") \
            .getOrCreate()
        
        print(f"--- เริ่มประมวลผลไฟล์ CSV: {csv_file_path} ---")

        # 3.3 อ่านไฟล์ CSV
        df_raw = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(csv_file_path)

        # แก้ไขชื่อคอลัมน์: 'timestamp' (จาก CSV) เป็น 'transaction_timestamp' (ที่ต้องการ)
        df_processed = df_raw.withColumnRenamed("timestamp", "transaction_timestamp")
        
        # --- เริ่ม Logic การเขียนข้อมูล ---

        # 1. เขียนข้อมูลทั้งหมดลงตาราง 'transactions' 
        # ใช้ 'append' เพื่อเลี่ยงปัญหา Foreign Key DROP
        write_dataframe_to_postgres(df=df_processed, table_name="transactions", write_mode="append") 

        # 2. กรองเฉพาะ Anomaly แล้วเขียนลงตาราง 'anomalies'
        df_anomalies_filtered = df_processed.filter(col("is_anomalous") == 1)

        # เลือกเฉพาะคอลัมน์ที่ต้องการสำหรับตาราง 'anomalies'
        df_anomalies_final = df_anomalies_filtered.select(
            "transaction_id",
            "user_id",
            "amount",
            "transaction_timestamp",
        )

        # เขียนตาราง anomalies
        write_dataframe_to_postgres(df=df_anomalies_final, table_name="anomalies", write_mode="append")
        
        # COMMIT TRANSACTION จะเกิดขึ้นเมื่อ Spark Session ถูกหยุดอย่างถูกต้อง
        print("--- การประมวลผลและการเขียนข้อมูลเสร็จสิ้น ---")

    except Exception as e:
        # พิมพ์ข้อความว่า Job ล้มเหลว (ถ้าเกิด Exception ภายใน try block)
        print(f"\n*** ERROR: การรัน PySpark Job ล้มเหลวอย่างสมบูรณ์ ***")
        # ไม่ re-raise ที่นี่แล้ว เพราะเราต้องการให้โปรแกรมไปที่ finally block
    
    finally:
        # สั่งหยุด SparkSession เสมอ เพื่อให้แน่ใจว่ามีการ Clean up และ COMMIT/ROLLBACK
        if spark is not None:
             spark.stop()