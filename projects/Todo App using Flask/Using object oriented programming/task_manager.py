from uuid import uuid4
from tasks import TASKS
from datetime import datetime


class TaskManager:
    def __init__(self):
        self.tasks = TASKS

    def get_all_tasks(self):
        keys = ["task_id", "task", "status"]

        all_tasks = []

        for task_details in self.tasks.values():
            task_details_to_return = {}
            for key, value in task_details.items():
                if key in keys:
                    task_details_to_return[key] = value

            all_tasks.append(task_details_to_return)

        response = {
            "tasks": all_tasks,
            "count": len(all_tasks)
        }

        return response

    def create_task(self, task_statement):
        task_id = str(uuid4())
        current_timestamp = datetime.now().isoformat()

        task = {
            "task_id": task_id,
            "task": task_statement,
            "created_at": current_timestamp,
            "last_updated_at": current_timestamp,
            "status": "In Progress"
        }

        self.tasks[task_id] = task
        return task

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def update_task(self, task_id, task_statement):
        task = self.tasks.get(task_id)

        if task and task["status"] != "Completed":
            task["task"] = task_statement
            task["last_updated_at"] = datetime.now().isoformat()
            return task

        return None

    def complete_task(self, task_id):
        task = self.tasks.get(task_id)

        if task:
            task["status"] = "Completed"
            task["last_updated_at"] = datetime.now().isoformat()
            return task

        return None

    def delete_task(self, task_id):
        return self.tasks.pop(task_id, None)
