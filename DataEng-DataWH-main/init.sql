-- DDL Script สำหรับสร้างตาราง PostgreSQL (ไฟล์ init.sql)

-- -------------------------------------------------------------------------
-- ตารางหลัก: transactions (เก็บข้อมูลธุรกรรมทั้งหมด)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(255) PRIMARY KEY, -- Primary Key
    
    user_id VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    product_category VARCHAR(100),
    
    transaction_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, 
    
    ip_address VARCHAR(50), 
    
    is_anomalous INTEGER NOT NULL, -- 1=ผิดปกติ, 0=ปกติ
    
    ingestion_time TIMESTAMP WITH TIME ZONE DEFAULT NOW() 
);

-- -------------------------------------------------------------------------
-- ตารางรอง: anomalies (เก็บเฉพาะข้อมูลที่ถูก flagged ว่าผิดปกติ)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS anomalies (
    transaction_id VARCHAR(255) PRIMARY KEY, -- Primary Key (ไม่จำเป็นต้องเป็น FK)
    
    user_id VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    transaction_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, 
    
    anomaly_type VARCHAR(50) DEFAULT 'Unspecified Anomaly' 
    
    -- ลบ Foreign Key Constraint ออกไป
    -- CONSTRAINT fk_transaction ...
);