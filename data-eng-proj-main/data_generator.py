# data_generator.py
from faker import Faker
import random
import uuid
from datetime import datetime

fake = Faker()

# --- การตั้งค่าสำหรับการสร้างข้อมูล ---
NORMAL_WEIGHT = 98 
ANOMALY_WEIGHT = 2  
NORMAL_AMOUNT_MAX = 1000.0
ANOMALY_AMOUNT_MIN = 5000.0 # กำหนดค่าสูงมาก
ANOMALY_AMOUNT_MAX = 15000.0

def generate_transaction():
    # 1. สุ่มกำหนดประเภทของธุรกรรม (Normal/Anomaly)
    is_anomaly_flag = random.choices([0, 1], weights=[NORMAL_WEIGHT, ANOMALY_WEIGHT])[0]
    
    amount = 0.0
    category = random.choice(["Electronics", "Fashion", "Home", "Beauty", "Toys"])
    
    if is_anomaly_flag == 1:
        # *** สร้าง Anomaly ด้วย amount ที่สูงมาก เพื่อให้ ML Model ตรวจจับได้ ***
        amount = round(random.uniform(ANOMALY_AMOUNT_MIN, ANOMALY_AMOUNT_MAX), 2)
    else:
        # สร้างธุรกรรมปกติ
        amount = round(random.uniform(5.0, NORMAL_AMOUNT_MAX), 2)

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "user_id": random.randint(1000, 9999),
        "amount": amount, # ใช้ค่า amount ที่กำหนดตามเงื่อนไข Anomaly แล้ว
        "product_category": category,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": fake.ipv4_public(),
        "is_anomalous": is_anomaly_flag 
    }
    return transaction

if __name__ == "__main__":
    for _ in range(5):
        print(generate_transaction())