# train_model.py (ใน data-eng-ml-main)
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import sys
import os

DATA_FILE = "historical_transactions.csv"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, 'anomaly_model.joblib')

def train_model():
    """
    Trains an Isolation Forest model using available features (amount, product_category) and saves it.
    """
    print(f"Loading data from {DATA_FILE}...")
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(f"🚨 Error: File not found at {DATA_FILE}")
        sys.exit(1)

    # ฟีเจอร์ที่ใช้: amount (Numeric) และ product_category (Categorical)
    feature_cols = ['amount', 'product_category']
    
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        print(f"🚨 Error: Missing required columns: {missing_cols}")
        print(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)

    # 1. เตรียมข้อมูล (Feature Engineering): One-Hot Encoding สำหรับ product_category
    print("Preparing data: Applying One-Hot Encoding to product_category...")
    
    # ใช้ One-Hot Encoding และ Drop the first category เพื่อป้องกัน multicollinearity
    df_processed = pd.get_dummies(df[feature_cols], columns=['product_category'], drop_first=True)
    
    features_final = df_processed.columns.tolist()
    X_train = df_processed
    
    print(f"Training on {len(X_train)} records using {len(features_final)} features.")

    # 2. สร้างและ Train Isolation Forest model
    # contamination=0.02 (ค่า Anomaly ที่เราสมมติว่ามีในข้อมูล)
    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42, n_jobs=-1)
    model.fit(X_train)

    print("✅ Model training complete.")

    # 3. สร้างโฟลเดอร์ 'model' และบันทึก model
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    joblib.dump(model, MODEL_PATH)
    
    print(f"💾 Model saved successfully to {MODEL_PATH}")
    
    # 4. บันทึกรายชื่อฟีเจอร์สุดท้ายที่ใช้ในการ train (สำคัญมากสำหรับ Spark App)
    with open(os.path.join(MODEL_DIR, 'model_features.txt'), 'w') as f:
        f.write('\n'.join(features_final))
    print("💾 Model features saved to model/model_features.txt")

if __name__ == "__main__":
    train_model()