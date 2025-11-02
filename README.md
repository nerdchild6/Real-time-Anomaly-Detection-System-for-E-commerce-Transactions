## Setup & Running the Pipeline

Follow these steps to deploy and run the entire real-time pipeline.

### 1. Initialize Docker Network
```bash
docker network create fraud_detection_network
```
### 2. Start PostgreSQL Database
```bash
cd DataEng-DataWH-main
docker compose up -d
```
### 3. Start Kafka & Zookeeper and Run the Producer
```bash
cd data-eng-proj-main
docker compose up -d
python producer.py
```
### 4. Run PySpark ML Streaming Application
```bash
cd data-eng-ml-main
docker compose up -d
```
### Verification & Debugging

Check Data in PostgreSQL
```bash
docker exec -it postgres_fraud_db psql -U postgres -d ecomm_fraud_db
```
Inside psql, run:
```bash
SELECT COUNT(*) FROM transactions;
SELECT COUNT(*) FROM anomalies;
```
