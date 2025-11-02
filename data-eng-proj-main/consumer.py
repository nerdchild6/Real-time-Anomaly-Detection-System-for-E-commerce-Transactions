from kafka import KafkaConsumer
import json
import pandas as pd

# Create Kafka Consumer
consumer = KafkaConsumer(
    'transactions',               # topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest', # read from beginning
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Optional: store messages into a list to create a DataFrame later
records = []

print("Consumer started... listening to Kafka topic 'transactions'")

try:
    for message in consumer:
        data = message.value
        print("Received:", data)

        # Store in memory (you can replace this with DB write)
        records.append(data)

        # Every 50 messages, save to CSV (optional)
        if len(records) % 50 == 0:
            df = pd.DataFrame(records)
            df.to_csv('consumed_transactions.csv', index=False)
            print("💾 Saved 50 messages to consumed_transactions.csv")

except KeyboardInterrupt:
    print(" Consumer stopped manually.")
    consumer.close()


