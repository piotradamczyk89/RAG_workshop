import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        request_body = json.loads(event['body'])
        names = request_body['names']
        for name in names:
            item = {"login": name,
                    "question": ""}
            boto3.resource('dynamodb').Table('workshop').put_item(Item=item)
        return {
            'statusCode': 200,
            'body': name
        }
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        return {
            "statusCode": 500,  # Internal Server Error
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"})
        }
