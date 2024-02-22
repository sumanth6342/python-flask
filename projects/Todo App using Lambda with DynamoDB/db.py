import json
from uuid import uuid4
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('todo')


def create_task(event):
    if "body" in event:
        body = event["body"]
        body = json.loads(body)

        if "task" in body:
            task_statement = body["task"]

            task_id = str(uuid4())
            current_timestamp = datetime.now().isoformat()

            task = {
                "data_type": "TODO",
                "task_id": task_id,
                "task": task_statement,
                "created_at": current_timestamp,
                "last_updated_at": current_timestamp,
                "status": "In Progress"
            }

            response = table.put_item(Item=task)

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "statusCode": 201,
                    "body": json.dumps(task)
                }

            else:
                error_mesage = {
                    "error": "Adding task failed"
                }

                return {
                    "statusCode": 500,
                    "body": json.dumps(error_mesage)
                }

        else:
            error_mesage = {
                "error": "Invalid request body"
            }

            return {
                "statusCode": 300,
                "body": json.dumps(error_mesage)
            }

    else:
        error_mesage = {
            "error": "Invalid request body"
        }

        return {
            "statusCode": 300,
            "body": json.dumps(error_mesage)
        }


def get_all_tasks():
    response = table.query(
        KeyConditionExpression=Key('data_type').eq('TODO'),

        # TODO: comes with additional cost, check the docs
        ConsistentRead=True
    )

    items = response["Items"]

    if items:
        all_tasks = []

        for item in items:
            task_details_to_return = {
                "task_id": item["task_id"],
                "task": item["task"],
                "status": item["status"]
            }

            all_tasks.append(task_details_to_return)

        response_data = {
            "tasks": all_tasks,
            "count": len(all_tasks)
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_data)
        }

    else:
        error_mesage = {
            "error": "No Tasks Found"
        }

        return {
            "statusCode": 400,
            "body": json.dumps(error_mesage)
        }


def get_a_task(path):
    task_id = path.split("/")[-1]

    response = table.get_item(
        Key={
            'data_type': 'TODO',
            'task_id': task_id
        },
        ConsistentRead=True
    )

    if "Item" in response:
        item = response["Item"]

        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    else:
        error_mesage = {
            "error": "Task id is invalid"
        }

        return {
            "statusCode": 400,
            "body": json.dumps(error_mesage)
        }


def complete_a_task(path):
    task_id = path.split("/")[-2]
    current_timestamp = datetime.now().isoformat()

    response = table.update_item(
        Key={
            'data_type': 'TODO',
            'task_id': task_id
        },
        UpdateExpression='SET #updateStatus = :updateStatus, #updateLastUpdated = :updateLastUpdated',
        ExpressionAttributeNames={
            '#updateStatus': "status",
            '#updateLastUpdated': "last_updated_at"
        },
        ExpressionAttributeValues={
            ':updateStatus': 'Completed',
            ':updateLastUpdated': current_timestamp
        }
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response_message = {
            "message": "Task completed"
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_message)
        }

    else:
        error_mesage = {
            "error": "Task id is invalid"
        }

        return {
            "statusCode": 400,
            "body": json.dumps(error_mesage)
        }


def delete_a_task(path):
    task_id = path.split("/")[-1]

    response = table.delete_item(
        Key={
            'data_type': 'TODO',
            'task_id': task_id
        }
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response_message = {
            "message": "Task deleted"
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_message)
        }

    else:
        error_mesage = {
            "error": "Task id is invalid"
        }

        return {
            "statusCode": 400,
            "body": json.dumps(error_mesage)
        }


def update_a_task(event):
    if "body" in event:
        body = event["body"]
        body = json.loads(body)

        if "task" in body:
            task_statement = body["task"]

            path = event["requestContext"]["http"]["path"]
            task_id = path.split("/")[-1]

            response = table.get_item(
                Key={
                    'data_type': 'TODO',
                    'task_id': task_id
                },
                ConsistentRead=True
            )

            if "Item" in response:
                item = response["Item"]
                status = item["status"]

                if status == "Completed":
                    error_mesage = {
                        "error": "Completed task cannot be updated"
                    }

                    return {
                        "statusCode": 400,
                        "body": json.dumps(error_mesage)
                    }

                else:
                    current_timestamp = datetime.now().isoformat()

                    response = table.update_item(
                        Key={
                            'data_type': 'TODO',
                            'task_id': task_id
                        },
                        UpdateExpression='SET #updateTask = :updateTask, #updateLastUpdated = :updateLastUpdated',
                        ExpressionAttributeNames={
                            '#updateTask': "task",
                            '#updateLastUpdated': "last_updated_at"
                        },
                        ExpressionAttributeValues={
                            ':updateTask': task_statement,
                            ':updateLastUpdated': current_timestamp
                        }
                    )

                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        response_message = {
                            "message": "Task updated"
                        }

                        return {
                            "statusCode": 200,
                            "body": json.dumps(response_message)
                        }

                    else:
                        error_mesage = {
                            "error": "Error updating task"
                        }

                        return {
                            "statusCode": 400,
                            "body": json.dumps(error_mesage)
                        }

            else:
                error_mesage = {
                    "error": "Task id is invalid"
                }

                return {
                    "statusCode": 400,
                    "body": json.dumps(error_mesage)
                }

        else:
            error_mesage = {
                "error": "Invalid request body"
            }

            return {
                "statusCode": 300,
                "body": json.dumps(error_mesage)
            }

    else:
        error_mesage = {
            "error": "Invalid request body"
        }

        return {
            "statusCode": 300,
            "body": json.dumps(error_mesage)
        }
