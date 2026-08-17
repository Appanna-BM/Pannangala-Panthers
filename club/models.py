import mysql.connector
from config import db_config

def get_connection():
    return mysql.connector.connect(**db_config)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team (
        member_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        position varchar(100) NOT NULL,
        designation varchar(100),
        join_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_us (
        contact_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE CHECk,
        
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
