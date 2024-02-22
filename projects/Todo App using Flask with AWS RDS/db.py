import psycopg2
DB_URL = "replace with your db host"


def get_connection():
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host=DB_URL,
        port='5432'
    )

    return connection


def run_query(connection, query, operation):
    data = None
    operation_success = False

    with connection.cursor() as cursor:
        cursor.execute(query)

        if operation == "select":
            data = cursor.fetchall()

        elif operation in ["insert", "delete", "update"]:
            connection.commit()
            if cursor.rowcount > 0:
                operation_success = True

    return data, operation_success


def execute_query(connection, query, operation):
    try:
        data, operation_success = run_query(connection, query, operation)

    except psycopg2.errors.lookup("25P02"):
        connection = get_connection()
        data, operation_success = run_query(connection, query, operation)

    return data, operation_success
