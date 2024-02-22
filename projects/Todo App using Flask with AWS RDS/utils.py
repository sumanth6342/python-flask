def generate_create_a_task_query(task):
    insert_keys = []
    insert_values = []

    for key, value in task.items():
        insert_keys.append(key)
        insert_values.append(f"'{value}'")

    insert_keys = ", ".join(insert_keys)
    insert_keys = f"({insert_keys})"

    insert_values = ", ".join(insert_values)
    insert_values = f"({insert_values})"

    query = f"""
    INSERT INTO tasks {insert_keys} 
    VALUES {insert_values}
    RETURNING *
    """
    return query
