#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: large_scale_crawling.py
@time: 4/10/21 12:54 PM
@desc:
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import argparse
import os
from google_play_scraper import Sort, reviews
import json

lock = threading.Lock()
lock_save = threading.Lock()
thread_num = 5
executor = ThreadPoolExecutor(max_workers=thread_num)
# finished_path = "data/finished.txt"


def get_package_list(package_list_path):
    apps = []
    with open(package_list_path, 'r') as file:
        for line in file:
            pkg_name = line.strip('\n')
            apps.append(pkg_name)
    return apps


def crawl_reviews(pkg_name, label, finished_list_path, save_path, num_reviews=100):
    print("work on:", pkg_name, label)
    results, _ = reviews(
        app_id=pkg_name,
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        count=num_reviews,
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=None  # defaults to None(means all score)
    )
    for res in results:
        if res['repliedAt'] is not None:
            res['repliedAt'] = res['repliedAt'].strftime("%Y-%m-%d %H:%M:%S")
        res['at'] = res['at'].strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        with open(finished_list_path, 'a+') as des:
            print(pkg_name, file=des)
    with lock_save:
        with open(save_path, 'a+') as save_file:
            print(json.dumps({"app_id": pkg_name, "label": int(label), "reviews": results}), file=save_file)
    return results


def get_finished(finished_path):
    return set(get_package_list(finished_path))


def main(package_list_path, finished_list_path, save_file_path):
    finished = get_finished(finished_list_path)
    print("finished: {}".format(len(finished)))
    with open(package_list_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                pkg_name, label = line.strip('\n').split(',')
                if pkg_name not in finished:
                    executor.submit(crawl_reviews, label=label, pkg_name=pkg_name,
                                    finished_list_path=finished_list_path, save_path=save_file_path)
                    while executor._work_queue.qsize() > thread_num:
                        time.sleep(1)
                else:
                    print("[*] did " + pkg_name)
    executor.shutdown(wait=True)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-p", "--pkg_list_path", type=str, required=True)
    # parser.add_argument("-f", "--finish_list_path", type=str, required=True)
    # parser.add_argument("-s", "--save_path", type=str, required=True)
    #
    # args = parser.parse_args()
    #
    # app_list_path = args.pkg_list_path
    # finished_apps_path = args.finish_list_path
    # save_path = args.save_path

    app_list_path = "data/package_label_list.csv"
    finished_apps_path = "data/finished.txt"
    save_path = "data/top_100_reviews_training.txt"

    main(package_list_path=app_list_path, finished_list_path=finished_apps_path, save_file_path=save_path)