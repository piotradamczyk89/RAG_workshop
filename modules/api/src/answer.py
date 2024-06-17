import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        return {
            'statusCode': 200,
            'body': "event"
        }
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        return {
            "statusCode": 500,  # Internal Server Error
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"})
        }
