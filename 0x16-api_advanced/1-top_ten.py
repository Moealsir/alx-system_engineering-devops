#!/usr/bin/python3
""" Function that queries the Reddit API """
import requests
import sys


def top_ten(subreddit):
    """Returns: top ten post titles
    or None if queried subreddit is invalid"""
    headers = {"User-Agent": "xica369"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    parameters = {"limit": 10}
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()
        titles_ = response.json().get("data", {}).get("children", [])
        for title_ in titles_:
            print(title_.get("data", {}).get("title"))
    except requests.RequestException as e:
        print(None)
