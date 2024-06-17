import json
import logging
import random

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        headers = event.get('headers', {})
        login = headers.get('login', 'error')
        if retrieve_user(login):
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('data_workshop')
            random_id = random.randint(1, 289)
            response = table.get_item(
                Key={
                    'id': random_id
                }
            )
            if 'Item' in response:
                random_question_id = random.randint(0, 2)
                info = response['Item']['data']['info']
                question = response['Item']['data']['questions'][random_question_id]
                user_record = {"login": login,
                               "question": {"info": info, "question": question}
                               }
                save_question(user_record)

                return {
                    'statusCode': 200,
                    "headers": {"Content-Type": "application/json"},
                    'body': json.dumps({"question": question})
                }
            else:
                return {
                    'statusCode': 200,
                    "headers": {"Content-Type": "application/json"},
                    'body': json.dumps({"error": "Wrong info item id. Contact the workshop leader "})
                }
        else:
            return {
                'statusCode': 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing header login or there is no user with provided login"})
            }
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        return {
            "statusCode": 500,  # Internal Server Error
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"})
        }


def retrieve_user(login):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('workshop')
    response = table.get_item(Key={"login": login})
    return 'Item' in response


def save_question(item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('workshop')
    table.put_item(Item=item)
