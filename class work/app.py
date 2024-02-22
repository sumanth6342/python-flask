import psycopg2
from uuid import uuid4
from datetime import datetime

from flask import Flask, request, jsonify
app = Flask(__name__)


def get_connection():
    connection = psycopg2.connect(
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
        host="demo-database.cluster-crikdn2kipwl.us-east-1.rds.amazonaws.com"
    )

    return connection


global_connection = get_connection()


def format_sql_records(tasks):
    formatted_tasks = {'tasks': []}

    formatted_tasks["count"] = len(tasks)

    for task_info in tasks:
        task_id, task, status = task_info

        task_dict = {
            "task_id": task_id,
            "task": task,
            "status": status,
        }

        formatted_tasks["tasks"].append(task_dict)

    return formatted_tasks


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    get_all_data_query = "SELECT task_id, task, status FROM task"

    tasks = []

    connection = global_connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(get_all_data_query)
            tasks = cursor.fetchall()

    except psycopg2.errors.lookup("25P02"):
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(get_all_data_query)
            tasks = cursor.fetchall()

    if tasks:
        print(f"{len(tasks)} fetched from the db")
        formatted_tasks = format_sql_records(tasks)
    else:
        formatted_tasks = {}

    if formatted_tasks:
        return jsonify(formatted_tasks), 200
    else:
        return jsonify({"error": "No Tasks Found"}), 400


app.run(
    debug=False,
    # port=80,
    # host="0.0.0.0"
)
