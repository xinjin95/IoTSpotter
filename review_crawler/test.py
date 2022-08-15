#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: test.py
@time: 4/10/21 12:28 PM
@desc:
"""
from google_play_scraper import app
import json
import datetime

from google_play_scraper import Sort, reviews, app, reviews_all


# def change_date_time(date_time_instance) -> str:
#     return date_time_instance.strftime("%Y-%m-%d %H:%M:%S")
# pkg_name = 'com.yunyi.smartcamera'
pkg_name = 'fr.climbingaway'


def test_review():
    continuation_token = None
    total = 0

    while True:
        result, continuation_token = reviews(
            app_id=pkg_name,
            lang='en',  # defaults to 'en'
            country='us',  # defaults to 'us'
            sort=Sort.RATING,  # defaults to Sort.MOST_RELEVANT
            filter_score_with=None,  # defaults to None(means all score)
            continuation_token=continuation_token
        )

        total += len(result)
        print(continuation_token, total)


def test_app():
    result = app(
        app_id=pkg_name
    )
    print(result)
    print(result["reviews"])


def test_review_all():
    result = reviews_all(
        app_id=pkg_name,
        sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST  # defaults to Sort.MOST_RELEVANT
        # filter_score_with=5  # defaults to None(means all score)
    )
    print(len(result))
    print(result[-1])


if __name__ == '__main__':
    # test_app()
    test_review_all()

# for i, res in enumerate(result):
#     print(i)
#     if i < 13:
#         continue
#     date_time = res['at']
#     # print(date_time)
#     date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
#     print(date_time)
#     res['at'] = date_time
#     res = json.dumps(res)
#     print(res)
    # for key, value in res.items():
    #     print(key, value)