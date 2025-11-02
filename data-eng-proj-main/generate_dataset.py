import pandas as pd
from data_generator import generate_transaction

records = [generate_transaction() for _ in range(100000)]
df = pd.DataFrame(records)
df.to_csv("historical_transactions.csv", index=False)

print("Saved 100k transaction dataset to historical_transactions.csv")
