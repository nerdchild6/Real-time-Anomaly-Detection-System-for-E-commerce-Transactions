```markdown
# 🛒 E-commerce Anomaly Detection Data Ingestion Pipeline

โปรเจกต์นี้คือ Data Pipeline ที่ใช้ **PySpark** ในการประมวลผลข้อมูล Transaction จากไฟล์ CSV และทำการจัดเก็บ (Ingestion) ข้อมูลเข้าสู่ฐานข้อมูล **PostgreSQL** โดยมีการแยกข้อมูลเป็น 2 ตารางหลัก คือ ข้อมูลธุรกรรมทั้งหมด (`transactions`) และข้อมูลธุรกรรมที่ผิดปกติ (`anomalies`)

---

## 🛠️ Tech Stack & Prerequisites

* **Orchestration/Execution:** Docker, Docker Compose
* **Big Data Processing:** Apache Spark (PySpark)
* **Database:** PostgreSQL
* **Driver:** PostgreSQL JDBC Driver

---

## 📦 โครงสร้างโปรเจกต์

```

.
├── docker-compose.yml
├── consumed\_transactions.csv  \# ไฟล์ข้อมูลดิบที่ใช้ทดสอบ
├── pyspark\_writer\_template.py \# โค้ด PySpark หลักสำหรับการ Ingestion
└── README.md                  \# ไฟล์เอกสารนี้

````

---

## 🚀 1. ขั้นตอนการติดตั้งและรันระบบ

### 1.1. สร้างและรัน Docker Containers

ใช้ `docker-compose` เพื่อสร้างและรัน PostgreSQL และ Spark Submit Container:

```bash
docker compose up -d
````

### 1.2. ตั้งค่า Database Schema (PostgreSQL)

เชื่อมต่อ DBeaver หรือเครื่องมืออื่น ๆ เข้ากับ PostgreSQL และสร้างตารางที่จำเป็น:

**Host:** `localhost:5432` | **DB:** `ecomm_fraud_db` | **User/Pass:** `postgres/123`

**คำสั่ง SQL สำหรับสร้างตาราง:**

```sql
-- 1. สร้างตารางแม่: transactions
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    is_anomalous INT
);

-- 2. สร้างตารางลูก: anomalies (ต้องมี Foreign Key ชี้ไปที่ transactions)
CREATE TABLE anomalies (
    anomaly_id SERIAL PRIMARY KEY,
    transaction_id INT UNIQUE NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);
```

### 1.3. รัน PySpark Ingestion Job

ใช้คำสั่ง `docker exec` เพื่อสั่งให้ Spark Submit Container รัน PySpark Job:

```bash
docker exec -it pyspark_submit_container spark-submit /app/pyspark_writer_template.py /app/consumed_transactions.csv
```

-----

## 📝 2. การทดสอบและตรวจสอบผลลัพธ์ (Verification)

### 2.1. การจัดการ DBeaver Session (สำคัญ)

เนื่องจาก DBeaver อาจมีปัญหา Caching ทำให้มองไม่เห็นข้อมูลที่เพิ่งถูก Commit ใหม่ **จำเป็นต้อง Disconnect และ Reconnect** การเชื่อมต่อกับฐานข้อมูลทุกครั้งก่อนตรวจสอบข้อมูล

### 2.2. การทดสอบการล้างและรันซ้ำ (End-to-End Test)

เพื่อทดสอบความเสถียรของระบบ (Append Test) โดยการล้างข้อมูลและรันซ้ำ 2 ครั้ง:

1.  **ล้างข้อมูล (ใน DBeaver):**
    ```sql
    TRUNCATE TABLE anomalies RESTART IDENTITY;
    TRUNCATE TABLE transactions RESTART IDENTITY CASCADE; 
    ```
2.  **รัน Job 2 ครั้ง:** (ทำซ้ำคำสั่งในข้อ 1.3 สองครั้ง)
3.  **ตรวจสอบผลลัพธ์รวม:** (หลังจาก Disconnect/Reconnect DBeaver แล้ว)
    ```sql
    SELECT count(*) FROM transactions; 
    -- ผลลัพธ์ที่คาดหวัง: 3600 (1800 rows x 2 runs)

    SELECT count(*) FROM anomalies;
    -- ผลลัพธ์ที่คาดหวัง: 76 (38 anomalies x 2 runs)
    ```

-----

## ⚠️ 3. การแก้ไขปัญหาที่สำคัญ (Troubleshooting)

ปัญหาหลักที่พบคือการ **Silent Rollback** เนื่องจาก Spark Job ไม่ได้สั่ง Commit:

  * **ปัญหา:** Log บอกว่าเขียนสำเร็จ แต่ DBeaver ไม่แสดงข้อมูล (COUNT = 0)
  * **สาเหตุ:** Transaction Rollback เนื่องจาก Job จบลงอย่างไม่สมบูรณ์ก่อนที่จะถึงจุด `spark.stop()`.
  * **วิธีแก้ไข:** ตรวจสอบว่าโค้ด **`pyspark_writer_template.py`** มีการเรียกใช้ **`spark.stop()`** ใน `finally` block เพื่อรับประกันการ Commit/Cleanup ที่ถูกต้อง

-----

*พัฒนาโดยใช้ PySpark และ PostgreSQL ภายใต้สภาพแวดล้อม Docker*

```
```
