import json
from uuid import uuid4
from datetime import datetime

from utils import (
    generate_create_a_task_query
)

from db import (
    get_connection,
    execute_query
)

from flask import Flask, request, jsonify
app = Flask(__name__)
connection = get_connection()

TASKS = []


@app.route("/tasks", methods=["POST"])
def create_task():
    request_data = request.json

    if "task" in request_data:
        task_id = str(uuid4())
        task_statement = request_data["task"]
        current_timestamp = datetime.now().isoformat()

        task = {
            "task_id": task_id,
            "task": task_statement,
            "created_at": current_timestamp,
            "last_updated_at": current_timestamp,
            "status": "In Progress"
        }

        query = generate_create_a_task_query(task)
        _, operation_success = execute_query(connection, query, "insert")

        if operation_success:
            return jsonify(task), 201
        else:
            return jsonify({"error": "Adding task failed"}), 500

    else:
        return jsonify({"error": "Invalid request body"}), 400


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    query = "SELECT task_id, task, status FROM tasks"
    data, _ = execute_query(connection, query, "select")

    if data:
        all_tasks = []

        for task_id, task, status in data:
            task_details_to_return = {
                "task_id": task_id,
                "task": task,
                "status": status
            }

            all_tasks.append(task_details_to_return)

        response = {
            "tasks": all_tasks,
            "count": len(all_tasks)
        }

        return jsonify(response), 200

    else:
        return jsonify({"error": "No Tasks Found"}), 400


@app.route("/tasks/<taskId>", methods=["GET"])
def get_a_task(taskId):
    query = f"SELECT * FROM tasks WHERE task_id = '{taskId}'"
    data, _ = execute_query(connection, query, "select")

    if data:
        task_id, task, created_at, last_updated_at, status = data[0]

        task = {
            "task_id": task_id,
            "task": task,
            "created_at": created_at,
            "last_updated_at": last_updated_at,
            "status": status
        }

        return jsonify(task), 200

    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>", methods=["PATCH"])
def update_a_task(taskId):
    request_data = request.json

    if "task" in request_data:
        task_statement = request_data["task"]
        current_timestamp = datetime.now().isoformat()

        query = f"""
        UPDATE tasks
        SET task = '{task_statement}', last_updated_at = '{current_timestamp}'
        WHERE task_id = '{taskId}'
        """

        response, _ = get_a_task(taskId)
        current_task = response.data.decode()
        current_task = json.loads(current_task)

        if current_task["status"] == "Completed":
            return jsonify({"error": "Completed task cannot be updated"}), 400

        _, operation_success = execute_query(connection, query, "delete")

        if operation_success:
            return jsonify({"message": "Task updated"}), 200
        else:
            return jsonify({"error": "Task id is invalid"}), 400
    else:
        return jsonify({"error": "Task is required"}), 400


@app.route("/tasks/<taskId>", methods=["DELETE"])
def delete_a_task(taskId):
    query = f"DELETE FROM tasks WHERE task_id = '{taskId}'"
    _, operation_success = execute_query(connection, query, "delete")

    if operation_success:
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>/complete", methods=["POST"])
def complete_a_task(taskId):
    current_timestamp = datetime.now().isoformat()

    query = f"""
    UPDATE tasks
    SET status = 'Completed', last_updated_at = '{current_timestamp}'
    WHERE task_id = '{taskId}'
    """

    _, operation_success = execute_query(connection, query, "update")

    if operation_success:
        return jsonify({"message": "Task completed"}), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


app.run(
    debug=True,
    # port=80,
    # host="0.0.0.0"
)
