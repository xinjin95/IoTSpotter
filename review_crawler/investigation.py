#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: investigation.py
@time: 4/10/21 10:06 PM
@desc:
"""
import json

keywords = ["permission", "bug", "login", "registration", "account", "register", "security", "secure", "leak",
            "password"]

with open("data/top_100_reviews_training.txt", 'r') as file:
    for line in file:
        js = json.loads(line)
        reviews = js["reviews"]
        if len(reviews) != 0:
            for review in reviews:
                content = review["content"]
                if content is None:
                    continue
                # print(content)
                matched = []
                for keyword in keywords:
                    if keyword in content:
                        matched.append(keyword)
                if len(matched) != 0:
                    print(matched, content)