import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Map doc_key to table names
TABLE_MAP = {
    "offer_letter": "offer_letter",
    "appointment_letter": "appointment_letters",
    "invoice": "invoice",
    "nda": "nda"
}

def fetch_document_data(doc_key, record_id):
    if doc_key not in TABLE_MAP:
        return None

    table_name = TABLE_MAP[doc_key]

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(f"DB error: {e}")
        return None
