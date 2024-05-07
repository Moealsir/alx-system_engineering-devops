#!/usr/bin/python3
"""
return top
"""
import requests


def top_ten(subreddit):
    """Returns the number of subscribers for a given subreddit"""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if not subreddit or type(subreddit) is not str:
        return None
    if response.status_code == 200:
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        if posts:
            for post in posts:
                print(post.get("data", {}).get("title"))
    else:
        print('None')
