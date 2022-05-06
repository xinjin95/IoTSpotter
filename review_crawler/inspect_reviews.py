#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: inspect_reviews.py
@time: 4/11/21 5:15 PM
@desc:
"""

import json

target_pkg = "com.facebook.orca"

with open("data/vt_reviews.txt", 'r') as file:
    for line in file:
        try:
            js = json.loads(line)
        except:
            js = None
            continue
        if len(js["reviews"]) < 10000:
            continue
        print(js['app_id'], len(js["reviews"]))
        if js['app_id'] == target_pkg:
            file_save_normal = open('data/com.facebook.orca_normal.txt', 'a+')
            file_save_anonymous = open('data/com.facebook.orca_anonymous.txt', 'a+')
            reviews = js["reviews"]
            for review in reviews:
                userImg = review["userImage"]
                user = review["userName"]
                if user == "A Google user":
                    print(userImg, file=file_save_anonymous)
                else:
                    print(userImg, file=file_save_normal)
        # reviews = js["reviews"]
        # users = set()
        # userImgs = set()
        # for review in reviews:
        #     # print(review['score'], "-", review['thumbsUpCount'], "-", review['userName'], "-", review['content'])
        #     user = review["userName"]
        #     userImg = review["userImage"]
        #     if user == "A Google user":
        #         continue
        #     if userImg in userImgs:
        #         print(userImg)
        #     userImgs.add(userImg)
        #     # if user in users:
        #     #     print(user)
        #     # users.add(user)
        # print("")