import json
import os
import pg8000
from datetime import datetime


class DatabaseConnector:
    def __init__(self):
        self.db_endpoint = os.getenv('DB_ENDPOINT')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_port = int(os.getenv('DB_PORT', '5432'))
        self.connection = None

    def connect(self):
        if not self.db_endpoint:
            raise ValueError('DB_ENDPOINT environment variable is not set.')
        
        print("Connecting to database...")
        self.connection = pg8000.connect(
            host=self.db_endpoint,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port
        )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")


class InventoryFetcher:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def fetch_all(self):
        conn = self.db_connector.connect()
        try:
            cursor = conn.cursor()
            select_query = "SELECT item_id, movement, quantity, timestamp FROM inventory_logs;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            cursor.close()
            return [
                {
                    "item_id": row[0],
                    "movement": row[1],
                    "quantity": row[2],
                    "timestamp": row[3].isoformat() if isinstance(row[3], datetime) else str(row[3])
                }
                for row in records
            ]
        finally:
            self.db_connector.close()


def lambda_handler(event, context):
    try:
        db_connector = DatabaseConnector()
        inventory_fetcher = InventoryFetcher(db_connector)

        inventory_data = inventory_fetcher.fetch_all()
        return {
            "statusCode": 200,
            "body": json.dumps(inventory_data)
        }
    except Exception as e:
        print(f"Error fetching inventory: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
