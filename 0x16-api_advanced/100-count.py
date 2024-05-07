#!/usr/bin/python3
"""
count
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

def count_words(subreddit, word_list, after="", word_frequency=None):
    """A function that retrieves hot articles.
    """
    if word_frequency is None:
        word_frequency = {word.lower(): 0 for word in word_list}

    if after is None:
        sorted_word_frequency = sorted(
            word_frequency.items(), key=lambda x: (-x[1], x[0])
        )
        for word, count in sorted_word_frequency:
            if count:
                print(f"{word}: {count}")
        return
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "reddit-query"}
    params = {"limit": 100, "after": after}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})
        posts = data.get("children", [])
        after = data.get("after")

        for post in posts:
            post_title = post["data"]["title"]
            words = post_title.lower().split()
            for word in word_list:
                word_frequency[word.lower()] += words.count(word.lower())

    except requests.RequestException:
        return None
    except Exception:
        return None

    count_words(subreddit, word_list, after, word_frequency)
