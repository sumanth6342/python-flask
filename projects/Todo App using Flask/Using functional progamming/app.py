from uuid import uuid4
from tasks import TASKS
from datetime import datetime

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    if TASKS:
        keys = ["task_id", "task", "status"]

        all_tasks = []

        for task_details in TASKS.values():
            task_details_to_return = {}
            for key, value in task_details.items():
                if key in keys:
                    task_details_to_return[key] = value

            all_tasks.append(task_details_to_return)

        response = {
            "tasks": all_tasks,
            "count": len(all_tasks)
        }

        return jsonify(response), 200

    else:
        return jsonify({"error": "No Tasks Found"}), 400


@app.route("/tasks", methods=["POST"])
def create_task():
    request_data = request.json

    if "task" in request_data:
        task_statement = request_data["task"]

        current_timestamp = datetime.now().isoformat()
        task_id = str(uuid4())

        task = {
            "task_id": task_id,
            "task": task_statement,
            "created_at": current_timestamp,
            "last_updated_at": current_timestamp,
            "status": "In Progress"
        }

        TASKS[task_id] = task
        return jsonify(task), 201

    else:
        return jsonify({"error": "Invalid request body"}), 400


@app.route("/tasks/<taskId>", methods=["GET"])
def get_a_task(taskId):
    if taskId in TASKS:
        task = TASKS[taskId]
        return jsonify(task), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>", methods=["PATCH"])
def update_a_task(taskId):
    request_data = request.json
    print(request_data)

    if "task" in request_data and taskId in TASKS:
        task_statement = request_data["task"]

        task = TASKS[taskId]
        status = task["status"]

        if status == "Completed":
            return jsonify({"error": "Completed task cannot be updated"}), 400

        task["task"] = task_statement
        task["last_updated_at"] = datetime.now().isoformat()

        return jsonify(task), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>/complete", methods=["POST"])
def complete_a_task(taskId):
    if taskId in TASKS:
        task = TASKS[taskId]

        task["status"] = "Completed"
        task["last_updated_at"] = datetime.now().isoformat()

        return jsonify(task), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>", methods=["DELETE"])
def delete_a_task(taskId):
    if taskId in TASKS:
        _ = TASKS.pop(taskId)
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


app.run(
    debug=True,
    # port=80,
    # host="0.0.0.0"
)
