#!/usr/bin/python3
"""export to json"""

import json
import requests
import sys


if __name__ == '__main__':
    if len(sys.argv) < 1:
        uid = sys.argv[1]
        url = 'https://jsonplaceholder.typicode.com/'
        user = requests.get(f'{url}users/{uid}').json()
        username = user.get('username')
        todos = requests.get(f'{user}/todos').json()
        tasks = [{'task': tasks.get('title'),
                  'completed': tasks.get('completed'),
                  'username': username} for tasks in todos]
        dict = {}
        dict[uid] = tasks
        with open(f'{uid}.json', 'w') as f:
            json.dump(dict, f)
    else:
        exit(1)
