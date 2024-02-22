from db import (
    create_task,
    get_all_tasks,
    get_a_task,
    complete_a_task,
    delete_a_task,
    update_a_task
)


def lambda_handler(event, context):
    if "requestContext" in event:
        method = event["requestContext"]["http"]["method"]
        path = event["requestContext"]["http"]["path"]

        if method == "POST":
            if path == "/tasks":
                return create_task(event)

            elif "/tasks/" in path and "complete" in path:
                return complete_a_task(path)

        elif method == "GET":
            if path == "/tasks":
                return get_all_tasks()

            elif "/tasks/" in path:
                return get_a_task(path)

        elif method == "DELETE" and "/tasks/" in path:
            return delete_a_task(path)

        elif method == "PATCH" and "/tasks/" in path:
            return update_a_task(event)

        else:
            return event
