#!/usr/bin/python3
"""export data in csv format"""

import csv
import requests
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        uid = sys.argv[1]
        url = 'https://jsonplaceholder.typicode.com/'
        req = requests.get(f'{url}users/{uid}')
        username = req.json().get('username')
        if username is not None:
            todos = requests.get(f'{url}users/{uid}/todos').json()
        with open(f'{uid}.csv', 'w', newline='') as f:
            write = csv.writer(f, quoting=csv.QUOTE_ALL)
            for task in todos:
                write.writerow([int(uid),
                                username,
                                task.get('complete'),
                                task.get('title')])
