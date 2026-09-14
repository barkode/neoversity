from sqlite3 import Error

from connect import create_connection, database


def select_projects(conn):
    """
    Query all rows in the task table
    :param conn: the connection object
    :return: rows objects
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT *  FROM projects;")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_all_tasks(conn):
    """
    Query all rows in the task table
    :param conn: the Connect object
    :return: rows tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks;")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_tasks_by_status(conn, status):
    """
    Query tasks by priority
    :param conn: the Connect object
    :param status:
    :return: rows tasks
    """

    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE staus=?", (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return rows


if __name__ == "__main__":
    with create_connection(database) as conn:
        print("Projects: ")
        projects = select_projects(conn)
        print(projects)
        print("Query all tasks: ")
        tasks = select_all_tasks(conn)
        print(tasks)
        print("Query tasks by status: ")
        task_by_priority = select_tasks_by_status(conn, True)
        print(task_by_priority)
