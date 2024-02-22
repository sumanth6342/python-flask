# pip install flask

from flask import Flask
app = Flask("ToDO")
# app = Flask(__name__)

HTTP = 80
HTTPS = 443


TASKS = {
    'a5437154-7593-4f87-81b7-8a867e00fac1': {
        'task_id': 'a5437154-7593-4f87-81b7-8a867e00fac1',
        'task': 'first task',
        'created_at': '2023-03-16T08:50:22.371911',
        'last_updated_at': '2023-03-16T08:50:22.371911',
        'status': 'In Progress'
    },

    'a432b999-5f5d-4662-bacd-dee8edbda7d7': {
        'task_id': 'a432b999-5f5d-4662-bacd-dee8edbda7d7',
        'task': 'Talk to karthik',
        'created_at': '2023-03-16T08:51:38.673934',
        'last_updated_at': '2023-03-16T08:51:38.673934',
        'status': 'In Progress'
    }
}


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    keys = ["task_id", "task", "status"]

    all_tasks = []

    for task_details in TASKS.values():
        task_details_to_return = {}
        for key, value in task_details.items():
            if key in keys:
                task_details_to_return[key] = value

        all_tasks.append(task_details_to_return)

    return all_tasks


app.run(
    debug=True,
    port=80,
    host="0.0.0.0"
)

# if __name__ == "__main__":
#     tasks = get_all_tasks()
#     print(tasks)


# tasks = get_all_tasks()
# print(tasks)

# print(dir(app))
# print(app)


# /tasks = > list all TASKS
# /task/taskid -> give a task
