from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy

POSTGRES_USER = 'expenselens_1'
POSTGRES_PASSWORD = 'expenselens_1'
POSTGRES_DB = 'user_object_mapping'
POSTGRES_CONNECTION_NAME = 'dcsc-lab-5-401318:us-east1:expenselens'

connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        POSTGRES_CONNECTION_NAME,
        "pg8000",
        user=POSTGRES_USER,
        db=POSTGRES_DB,
        password=POSTGRES_PASSWORD,
        enable_iam_auth=True,
    )
    return conn

def create_user_images_table(pool):
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS user_images (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255),
                image_path VARCHAR(255)
            )
        """)
        db_transaction.commit()

def insert_user_image(pool, user_name, gcs_blob_name):
    insert_stmt = sqlalchemy.text(
        "INSERT INTO user_images (username, image_path) VALUES (:username, :image_path)"
    )
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute(insert_stmt, {"username": user_name, "image_path": gcs_blob_name})
        db_transaction.commit()
        
def create_authentication_table(pool):
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS authentication (
                username VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255)
            )
        """)
        db_transaction.commit()

def insert_authentication_details(pool, user_name, password):
    insert_stmt = sqlalchemy.text(
        "INSERT INTO authentication (username, password) VALUES (:username, :password)"
    )
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute(insert_stmt, {"username": user_name, "password": password})
        db_transaction.commit()
        
def create_receipt_details_table(pool):
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS receipt_details_2 (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255),
                receipt_id INTEGER REFERENCES user_images(id),
                category VARCHAR(50),
                merchant_name VARCHAR(255),
                city VARCHAR(50),
                state VARCHAR(50),
                country VARCHAR(50),
                date VARCHAR(50),
                product_details JSON,
                total_amount DOUBLE PRECISION,
                sub_total_amount DOUBLE PRECISION,
                tax DOUBLE PRECISION
            )
        """)
        db_transaction.commit()

def insert_receipt_details(pool, user_id, username, receipt_details):
    
    insert_stmt = sqlalchemy.text(
        "INSERT INTO receipt_details_2 (username, receipt_id, category, merchant_name, city, state, country, date, product_details, total_amount, sub_total_amount, tax) VALUES (:username, :receipt_id, :category, :merchant_name, :city, :state, :country, :date, :product_details, :total_amount, :sub_total_amount, :tax)"
    )
    with pool.connect() as db_conn:
        db_transaction = db_conn.begin()
        db_conn.execute(insert_stmt, {"username": username, "receipt_id": int(user_id), "category": receipt_details["category"], "merchant_name": receipt_details["merchant_name"], "city": receipt_details["city"], "state": receipt_details["state"], "country": receipt_details["country"], "date": receipt_details["date"], "product_details": receipt_details["product_details"], "total_amount": float(receipt_details["total_amount"]), "sub_total_amount": float(receipt_details["sub_total_amount"]), "tax": float(receipt_details["tax"])})
        db_transaction.commit()
        
def closeConnection():
    connector.close()
