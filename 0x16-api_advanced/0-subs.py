#!/usr/bin/python3
import requests


def number_of_subscribers(subreddit):
    """Returns the number of subscribers for a given subreddit"""

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("data").get("subscribers")
    else:
        return 0
