import os
import mysql.connector
from mysql.connector import Error

# ---------------------------------------------------
# Load .env from ROOT DIRECTORY (same as app.py)
# ---------------------------------------------------
ROOT_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
from dotenv import load_dotenv
load_dotenv(ROOT_ENV_PATH)

from config import Config


# ---------------------------------------------------
# CREATE DATABASE IF NOT EXISTS
# ---------------------------------------------------
def create_database_if_missing():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✔ Database '{Config.DB_NAME}' verified/created.")
    except Exception as e:
        print("❌ Database creation failed:", e)


# ---------------------------------------------------
# GET CONNECTION TO DATABASE
# ---------------------------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except Error as e:
        print("❌ DATABASE CONNECTION FAILED:", e)
        return None


# ---------------------------------------------------
# CREATE ALL TABLES
# ---------------------------------------------------
def create_tables():
    conn = get_db_connection()
    if not conn:
        print("⚠ TABLE CREATION SKIPPED — No DB connection")
        return

    cursor = conn.cursor()

    tables = [

        # USERS TABLE
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            mobile VARCHAR(20),
            email VARCHAR(150),
            college_id VARCHAR(50),
            role ENUM('master','super_admin','admin','student') NOT NULL,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(255),
            selfie VARCHAR(255),
            college_id_card VARCHAR(255),
            aadhar_student VARCHAR(255),
            aadhar_parent VARCHAR(255),
            health_issue TEXT,
            is_verified TINYINT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # GEOFENCE TABLE (now includes expires_at)
        """
        CREATE TABLE IF NOT EXISTS geofence (
            id INT AUTO_INCREMENT PRIMARY KEY,
            landmark VARCHAR(150),
            latitude DOUBLE,
            longitude DOUBLE,
            radius INT DEFAULT 200,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NULL
        );
        """,

        # ATTENDANCE TABLE
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            geofence_id INT,
            status ENUM('present','absent'),
            marked_lat DOUBLE,
            marked_lng DOUBLE,
            distance DOUBLE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (geofence_id) REFERENCES geofence(id) ON DELETE SET NULL
        );
        """,

        # UPLOADS TABLE
        """
        CREATE TABLE IF NOT EXISTS uploads (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            file_path VARCHAR(255),
            description TEXT,
            uploaded_by_role VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """,

        # NOTIFICATIONS TABLE
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150),
            message TEXT,
            send_to ENUM('all','student','admin','super_admin'),
            sender_id INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """,

        # ACTIVITY LOG
        """
        CREATE TABLE IF NOT EXISTS activity_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            activity TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """
    ]

    # Execute each table creation cleanly
    for query in tables:
        cursor.execute(query)
        conn.commit()

    cursor.close()
    conn.close()

    print("✔ All tables created successfully.")


# ---------------------------------------------------
# DEFAULT USERS (Master + Super Admin)
# ---------------------------------------------------
def seed_default_users():
    conn = get_db_connection()
    if not conn:
        print("⚠ SEED SKIPPED — No DB connection")
        return

    cursor = conn.cursor(dictionary=True)

    # CREATE MASTER IF MISSING
    cursor.execute("SELECT id FROM users WHERE role='master' LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (name, mobile, email, college_id, role, username, password, is_verified)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            "Master User",
            "0000000000",
            "master@venus.com",
            "MASTER001",
            "master",
            "master",
            "master123",
            1
        ))
        conn.commit()
        print("✔ Default MASTER created")

    # CREATE SUPER ADMIN IF MISSING
    cursor.execute("SELECT id FROM users WHERE role='super_admin' LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (name, mobile, email, college_id, role, username, password, is_verified)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            "College Director",
            "1111111111",
            "director@venus.com",
            "DIRECTOR001",
            "super_admin",
            "director",
            "director123",
            1
        ))
        conn.commit()
        print("✔ Default SUPER ADMIN created")

    cursor.close()
    conn.close()


# ---------------------------------------------------
# RUN DB SETUP
# ---------------------------------------------------
try:
    create_database_if_missing()
    create_tables()
    seed_default_users()
except Exception as e:
    print("❌ DB SETUP ERROR:", e)
