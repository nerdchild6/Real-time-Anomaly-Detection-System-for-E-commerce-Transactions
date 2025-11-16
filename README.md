# Real-time E-commerce Anomaly Detection System

This university project demonstrates a complete, end-to-end **real-time data pipeline** for detecting fraudulent or anomalous e-commerce transactions.

The system uses a modern event-driven architecture powered by:

- **Apache Kafka** – real-time data ingestion  
- **Apache Spark (PySpark)** – stream processing & ML scoring  
- **PostgreSQL** – persistent storage  
- **Metabase** – live dashboarding  
- **Docker Compose** – service orchestration  

---

## 📊 Dashboard Preview

A live dashboard showing:

- Key transaction metrics  
- Real-time feed of flagged anomalies  

---

## 🚨 The Problem

Fraud detection in e-commerce is often performed as **batch analysis**, meaning anomalies are detected hours or days later—when it's too late to stop fraudulent orders.

---

## ✅ Our Solution

We built a **real-time, proactive fraud detection system**:

- Ingests incoming transactions instantly  
- Scores each transaction using a pre-trained **Isolation Forest (scikit-learn)** model  
- Flags transactions as **normal** or **anomalous**  
- Streams enriched results to PostgreSQL  
- Visualizes them in Metabase with auto-refresh  

This enables immediate action on high-risk transactions.

---

## 🏗️ System Architecture

All components run as independent Docker services managed via **Docker Compose**.

### 🔄 Data Flow

1. **Ingest (Kafka)**  
   - `producer.py` generates synthetic transactions using `Faker` library  
   - Publishes JSON messages to Kafka topic: `transactions`

2. **Process (Spark)**  
   - PySpark Structured Streaming consumes the Kafka topic

3. **Enrich (ML)**  
   - Spark loads a pre-trained Isolation Forest model  
   - Adds a boolean prediction column: `is_anomaly`

4. **Store (PostgreSQL)**  
   - Spark writes enriched records into the database

5. **Visualize (Metabase)**  
   - Metabase queries the PostgreSQL table
   - Updates charts and anomaly feed
<img width="1920" height="1080" alt="Real-time E-commerce Anomaly Detection" src="https://github.com/user-attachments/assets/d1fb7b1a-7a7b-4909-8e79-44fea2f9db6a" />

---

## 🧰 Tech Stack

| Category            | Tool                | Purpose                                                    |
|--------------------|---------------------|------------------------------------------------------------|
| Orchestration       | Docker Compose      | Manages multi-container environment                        |
| Data Ingestion      | Apache Kafka        | Real-time message streaming                                |
| Stream Processing   | Apache Spark        | Distributed processing of live data                        |
| Machine Learning    | Scikit-learn        | IsolationForest anomaly detection model                    |
| Data Storage        | PostgreSQL          | Stores enriched transaction data                           |
| Visualization       | Metabase            | Dashboard for real-time insights                           |
| Database Client     | DBeaver             | Used for schema design and validation                      |

---

## 🚀 How to Run This Project

Follow these steps to deploy and run the entire real-time pipeline.

### 1. Start the Project
```bash
docker compose up -d --build
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
quit psql, run:
```bash
exit
```

### 2. Show the result(Metabase)
To see the results of the fraud detection, you can create the dashboard in *Metabase*.
- Open your browser and go to `http://localhost:3000`
- Follow the setup instructions to create an admin account.
- Connect to the PostgreSQL database.

| Step1: Go to database  | Step2: Create PostgreSQL connection |
| :---: | :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 221557" src="https://github.com/user-attachments/assets/900e8dc5-e1ef-44dc-9224-f6d756aa6a35" /> | <img width="960" height="505" alt="image" src="https://github.com/user-attachments/assets/0eae0761-4052-4228-b7ff-bd908c005a03" /> | 
- Using the following details:
    - Database type: `PostgreSQL`
    - Display name: (up to you)
    - Host: `postgres_db`
    - Port: `5432`
    - Database Name: `ecomm_fraud_db`
    - Username: `postgres`
    - Password: `123`

| Step3: Exit Admin mode |
| :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 233255" src="https://github.com/user-attachments/assets/a77c6fec-54c6-4fd8-ae3b-fae0944c8eaa" /> |

- Once connected, you can create questions and dashboards to visualize the fraud detection results. For example: create simple graph

| Step1: Go to database  | Step2: Select database you want | Step3: Select table | 
| :---: | :---: | :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 221557" src="https://github.com/user-attachments/assets/900e8dc5-e1ef-44dc-9224-f6d756aa6a35" /> | <img width="960" height="505" alt="Screenshot 2025-11-02 221846" src="https://github.com/user-attachments/assets/61f31e19-69e0-44ee-85fa-289cf5058bdd" /> | <img width="960" height="505" alt="Screenshot 2025-11-02 221916" src="https://github.com/user-attachments/assets/2a7af0bb-e0ea-406e-9867-f51de96361ec" /> | 

| Step4: Click 'Visualization' | Step5: Click 'Summarize' | Step6: Click 'Amount' column |
| :---: | :---: | :---: |
| <img width="960" height="504" alt="Screenshot 2025-11-02 222002" src="https://github.com/user-attachments/assets/e3434eef-9012-42ab-9c40-53f9704b97c6" /> |  <img width="960" height="504" alt="Screenshot 2025-11-02 222220" src="https://github.com/user-attachments/assets/3deddf59-ba7b-4588-b7e1-30ec02be6923" /> | <img width="960" height="503" alt="Screenshot 2025-11-02 222316" src="https://github.com/user-attachments/assets/db34ad4a-83e1-4d84-a67a-2047184aa4fa" /> |

| Step7: Click 'Done' | Step8: Click 'Save' | Step9: Config as you want and click 'Save' |
| :---: | :---: | :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 222426" src="https://github.com/user-attachments/assets/8b5a4cd5-68d4-4885-84f6-f34a941825cd" /> | <img width="960" height="504" alt="Screenshot 2025-11-02 222520" src="https://github.com/user-attachments/assets/c9d96f91-91e6-45b6-847f-3d141371086d" /> | <img width="960" height="503" alt="Screenshot 2025-11-02 222737" src="https://github.com/user-attachments/assets/013f61bc-fa2b-4d90-8b2d-5a26b048609a" /> |

| Step10: Simple graph are show |
| :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 222838" src="https://github.com/user-attachments/assets/17eabe45-dedd-4035-8ef8-e32a67a9c7d4" /> |

### Stop the Project
```bash
docker compose down
```
### Additional Notes
- Ensure Docker and Docker Compose are installed on your machine.
- Logs for each service can be viewed using:
```bash
docker logs <service_name>
```
### Troubleshooting
- If you encounter issues with Kafka, ensure that the Kafka and Zookeeper services are running properly
- For database connection issues, verify the connection details and ensure the PostgreSQL service is up and running
- Check the logs of individual services for more detailed error messages.
### Clean Up
To remove all Docker containers, networks, and volumes created by the project, run:
```bash
docker-compose down --volumes
```
This will help you free up space and ensure a clean state for future deployments.

---
## 📁 Project Structure & Team Roles

This project was built by a 5-person team, with each member responsible for a critical part of the real-time data pipeline.

---

### 🧩 `docker-compose.yml`  
**Team Lead & Data Architect — [Worrawit Klangsaeng]**  
- Master orchestration file that defines and manages all Docker services.

---

### 📦 `producer/`  
**Data Source & Ingestion Engineer — [Yoon Thedar Cho]**

- **`producer.py`** – Generates synthetic e-commerce transactions using `Faker` library and publishes them to Kafka via `kafka-python`.  
- **`Dockerfile`** – Containerizes the producer service.

---

### ⚙️ `spark-app/`  
**Machine Learning & Processing Engineer — [Thanapat Nasa]**

- **`app.py`** – PySpark Structured Streaming application connecting Kafka → Spark → PostgreSQL.  
- **`model/isolation_forest.joblib`** – Pre-trained Isolation Forest model (scikit-learn).  
- **`Dockerfile`** – Container for the Spark job and dependencies.

---

### 🗄️ `database/`  
**Database & Data Storage Engineer — [Engkatuch Sombatkumjorn]**

- **`init.sql`** – Initializes the PostgreSQL schema and creates the `transactions` table at startup.

---

### 📊 `dashboard/`  
**Dashboard & Reporting Engineer — [Pornprom Ounsuchat]**

- Responsible for SQL queries and Metabase dashboards  
- Builds the real-time visualization for anomalies and key metrics.

---

## 🔮 Future Work

### ☁️ Deploy to Cloud  
Migrate the full Docker Compose stack to AWS ECS, GCP Cloud Run, or another cloud provider to achieve production-level scalability.

### 🚨 Real-time Alerting  
Create a new microservice that consumes from an `anomalies` Kafka topic and sends Slack or email alerts instantly.

### 🤖 Advanced Machine Learning  
Implement stateful or deep learning models (e.g., Autoencoders, LSTM) directly in Spark ML to detect more complex fraudulent behavior patterns.



