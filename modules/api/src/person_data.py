import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        request_body = json.loads(event['body'])
        datas = request_body['persons']

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('data_workshop')

        response = table.scan(ProjectionExpression="id")
        items = response['Items']

        if items:
            max_id = max((item['id']) for item in items)
        else:
            max_id = 0

        items = []

        logger.info("id maks to")
        logger.info(max_id)

        for data in datas:
            max_id += 1
            items.append({"id": max_id, "data": data})

        logger.info(items)

        for chunk in chunk_data(items):
            batch_write_items(table, chunk)

        return {
            'statusCode': 200,
            'body': json.dumps({"result": 'Items added successfully!'})
        }
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        return {
            "statusCode": 500,  # Internal Server Error
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"})
        }


def chunk_data(data, chunk_size=25):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def batch_write_items(table, items):
    try:
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    except ClientError as e:
        print(f"Error occurred: {e}")
