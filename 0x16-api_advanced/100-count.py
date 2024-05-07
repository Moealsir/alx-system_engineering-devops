#!/usr/bin/python3
"""
count
"""
import requests
from 2-recurse import recurse


def count_words(subreddit, word_list, count_dict=None):
    if count_dict is None:
        count_dict = {}

    # Recursively fetch hot articles
    hot_list = recurse(subreddit)

    if hot_list is None:
        return

    # Count occurrences of keywords in titles
    for title in hot_list:
        for word in title.lower().split():
            if word in word_list:
                count_dict[word] = count_dict.get(word, 0) + 1

    sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")
