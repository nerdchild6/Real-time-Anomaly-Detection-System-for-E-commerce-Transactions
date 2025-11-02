from kafka import KafkaProducer
import json
import time
from data_generator import generate_transaction

# การตั้งค่า: 'localhost:9092' ถูกต้องแล้วสำหรับการรัน Producer นอก Docker 
# เพื่อเชื่อมต่อกับพอร์ตที่ถูก Expose ของ Container Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = "transactions"

print("🚀 Kafka Producer started. Attempting connection to localhost:9092...")

while True:
    data = generate_transaction()
    try:
        # 1. ส่งข้อมูลแบบ Asynchronous
        future = producer.send(topic_name, value=data)
        
        # 2. **สำคัญ:** บังคับให้รอจนกว่าจะส่งเสร็จ (Synchronous) ภายใน 10 วินาที
        # ถ้าส่งไม่สำเร็จภายในเวลาที่กำหนด จะเกิด Exception
        future.get(timeout=10) 
        
        print("✅ Sent:", data)
    
    except Exception as e:
        # หากเกิดข้อผิดพลาดในการเชื่อมต่อหรือส่งข้อมูล จะแสดงข้อความนี้
        print(f"🚨 ERROR: Failed to send message to Kafka. Check if Kafka is running: {e}")
        # หยุดรอ 5 วินาทีก่อนลองส่งใหม่
        time.sleep(5) 
    
    # หน่วงเวลา 1 วินาทีต่อการส่ง 1 ธุรกรรม
    time.sleep(1)