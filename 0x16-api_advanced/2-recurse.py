#!/usr/bin/python3
"""
return top
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Returns the number of subscribers for a given subreddit"""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": 100, "after": after} if after else {"limit": 100}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        for post in posts:
            hot_list.append(post["data"]["title"])

        after = data["data"].get("after")

        if after:
            return recurse(subreddit, hot_list, after)
        return hot_list
    return None
