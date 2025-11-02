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


