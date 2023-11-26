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
        
def closeConnection():
    connector.close()
