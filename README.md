## Setup & Running the Pipeline

Follow these steps to deploy and run the entire real-time pipeline.

### 1. Train the Model (One-time setup)
Before running the pipeline, you need to train the model first.
```bash
cd data-eng-ml-main
pip install -r requirements.txt
python train_model.py
```
### 2. Start the Project
```bash
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
### 3. Show the result(Metabase)
To see the results of the fraud detection, you can create the dashboard in *Metabase*.
- Open your browser and go to `http://localhost:3000`
- Follow the setup instructions to create an admin account.
- Connect to the PostgreSQL database using the following details:
    - Database type: `PostgreSQL`
    - Host: `postgres_db`
    - Port: `5432`
    - Database Name: `ecomm_fraud_db`
    - Username: `postgres`
    - Password: `123`
- Once connected, you can create questions and dashboards to visualize the fraud detection results.

| Step1 | Step2 | Step3| 
| :---: | :---: | :---: |
| <img width="960" height="505" alt="Screenshot 2025-11-02 221557" src="https://github.com/user-attachments/assets/900e8dc5-e1ef-44dc-9224-f6d756aa6a35" />
| <img width="300" alt="Good nutrition result" src="https://github.com/user-attachments/assets/031748b5-9eb9-43b7-9524-9e3ab5432e76" /> 
| <img width="300" alt="Poor nutrition result" src="https://github.com/user-attachments/assets/133bb978-7ef7-4d7b-b1a4-8223f215b56b" /> 
| 
|

### 4. Stop the Project
```bash
docker compose down
```
### 5. Additional Notes
- Ensure Docker and Docker Compose are installed on your machine.
- The model training step is a one-time process; you don't need to retrain the model for each deployment
- Logs for each service can be viewed using:
```bash
docker logs <service_name>
```
### 6. Troubleshooting
- If you encounter issues with Kafka, ensure that the Kafka and Zookeeper services are running properly
- For database connection issues, verify the connection details and ensure the PostgreSQL service is up and running
- Check the logs of individual services for more detailed error messages.
### 7. Clean Up
To remove all Docker containers, networks, and volumes created by the project, run:
```bash
docker-compose down --volumes
```
This will help you free up space and ensure a clean state for future deployments.


