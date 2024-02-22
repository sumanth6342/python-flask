from flask import Flask, request, jsonify
from task_manager import TaskManager
tm = TaskManager()
app = Flask(__name__)


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = tm.get_all_tasks()

    if tasks:
        return jsonify(tasks), 200
    else:
        return jsonify({"error": "No Tasks Found"}), 400


@app.route("/tasks", methods=["POST"])
def create_task():
    request_data = request.json

    if "task" in request_data:
        task_statement = request_data["task"]
        task = tm.create_task(task_statement)
        return jsonify(task), 201

    else:
        return jsonify({"error": "Invalid request body"}), 400


@app.route("/tasks/<taskId>", methods=["GET"])
def get_a_task(taskId):
    task = tm.get_task(taskId)

    if task:
        return jsonify(task), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>", methods=["PATCH"])
def update_a_task(taskId):
    request_data = request.json

    if "task" in request_data:
        task_statement = request_data["task"]
        task = tm.update_task(taskId, task_statement)

        if task:
            return jsonify(task), 200
        else:
            return jsonify({"error": "Completed task cannot be updated"}), 400

    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>/complete", methods=["POST"])
def complete_a_task(taskId):
    task = tm.complete_task(taskId)

    if task:
        return jsonify(task), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


@app.route("/tasks/<taskId>", methods=["DELETE"])
def delete_a_task(taskId):
    task_id = tm.delete_task(taskId)

    if task_id:
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Task id is invalid"}), 400


app.run(
    debug=True,
    # port=80,
    # host="0.0.0.0"
)
