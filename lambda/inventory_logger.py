import json
import os
import pg8000

def lambda_handler(event, context):
    db_endpoint = os.getenv('DB_ENDPOINT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = int(os.getenv('DB_PORT', '5432'))

    # Check if the endpoint is properly received
    if not db_endpoint:
        return {
            'statusCode': 500,
            'body': json.dumps('DB_ENDPOINT environment variable is not set.')
        }
    
    try:
        payload = json.loads(event['body']) 
        item_id = payload.get('item_id')
        movement = payload.get('movement')
        quantity = payload.get('quantity')
        timestamp = payload.get('timestamp')

        if not all([item_id, movement, quantity, timestamp]):
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required data fields.')
            }

    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid data format: {str(e)}')
        }

    try:
        conn = pg8000.connect(
            host=db_endpoint,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = conn.cursor()

        insert_query = '''INSERT INTO inventory_logs (item_id, movement, quantity, timestamp) 
                          VALUES (%s, %s, %s, %s);'''
        cursor.execute(insert_query, (item_id, movement, quantity, timestamp))
        conn.commit()

        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Data stored successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Database connection failed: {str(e)}')
        }
