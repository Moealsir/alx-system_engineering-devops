#!/usr/bin/python3
"""export data in the JSON format"""

import json
import requests


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"
    users = requests.get(f"{url}users/").json()
    userj = {}
    for user in users:
        uid = user.get("id")
        username = user.get("username")
        todos = requests.get(f"{url}users/{uid}/todos").json()
        task = [
            {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed"),
            }
            for task in todos
        ]
        userj[uid] = task
        with open("todo_all_employees.json", "w") as f:
            json.dump(userj, f)
