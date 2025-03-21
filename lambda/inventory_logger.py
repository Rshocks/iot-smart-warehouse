import json
import os
import pg8000


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


class InventoryLogger:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def log(self, item_id, movement, quantity, timestamp):
        conn = self.db_connector.connect()
        try:
            cursor = conn.cursor()
            insert_query = '''INSERT INTO inventory_logs (item_id, movement, quantity, timestamp) 
                              VALUES (%s, %s, %s, %s);'''
            cursor.execute(insert_query, (item_id, movement, quantity, timestamp))
            conn.commit()
        finally:
            cursor.close()
            self.db_connector.close()


class RequestHandler:
    @staticmethod
    def parse_event(event):
        try:
            payload = json.loads(event['body'])
            item_id = payload.get('item_id')
            movement = payload.get('movement')
            quantity = payload.get('quantity')
            timestamp = payload.get('timestamp')

            if not all([item_id, movement, quantity, timestamp]):
                return None, 'Missing required data fields.'

            return (item_id, movement, quantity, timestamp), None
        except (json.JSONDecodeError, KeyError) as e:
            return None, f'Invalid data format: {str(e)}'


def lambda_handler(event, context):
    db_connector = DatabaseConnector()
    inventory_logger = InventoryLogger(db_connector)

    data, error = RequestHandler.parse_event(event)
    if error:
        return {
            'statusCode': 400,
            'body': json.dumps(error)
        }

    try:
        item_id, movement, quantity, timestamp = data
        inventory_logger.log(item_id, movement, quantity, timestamp)

        return {
            'statusCode': 200,
            'body': json.dumps('Data stored successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Database connection failed: {str(e)}')
        }
