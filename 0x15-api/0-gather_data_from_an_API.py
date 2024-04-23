#!/usr/bin/python3
""" Gather data from an API """
import requests
import sys


def to_do_list(emp_id):
    """ Fetches employee TODO list """

    url = "https://jsonplaceholder.typicode.com/users"
    req = requests.get(f"{url}/{emp_id}")
    data = req.json()
    name = data.get("name")

    if name is not None:
        user_todo = requests.get(f"{url}/{emp_id}/todos")
        user_todos = user_todo.json()
        tasks_num = len(user_todos)
        t_finished = []

        for task in user_todos:
            if task.get("completed") is True:
                t_finished.append(task)
        num_t_finished = len(t_finished)
        print("Employee {} is done with tasks ({}/{}):".
              format(name, num_t_finished, tasks_num))

        for task in t_finished:
            title = task.get("title")
            print(f"\t {title}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    EMPLOYEE_ID = int(sys.argv[1])
    to_do_list(EMPLOYEE_ID)
