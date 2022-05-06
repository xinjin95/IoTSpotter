#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
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
from google_play_scraper import Sort, reviews, reviews_all
import json

lock = threading.Lock()
lock_save = threading.Lock()
thread_num = 10
executor = ThreadPoolExecutor(max_workers=thread_num)
# finished_path = "data/finished.txt"


def get_package_list(package_list_path):
    apps = []
    with open(package_list_path, 'r') as file:
        for line in file:
            pkg_name = line.strip('\n')
            apps.append(pkg_name)
    return apps


def crawl_reviews(pkg_name, finished_list_path, save_path):
    print("work on:", pkg_name)
    results = reviews_all(
        app_id=pkg_name,
        sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST  # defaults to Sort.MOST_RELEVANT
        # filter_score_with=5  # defaults to None(means all score)
    )
    if len(results) != 0:
        print(pkg_name, len(results))
        for res in results:
            if res['repliedAt'] is not None:
                res['repliedAt'] = res['repliedAt'].strftime("%Y-%m-%d %H:%M:%S")
            res['at'] = res['at'].strftime("%Y-%m-%d %H:%M:%S")
        with lock_save:
            with open(save_path, 'a+') as save_file:
                print(json.dumps({"app_id": pkg_name, "reviews": results}), file=save_file)
                print("[-] save:", pkg_name)
        return results
    for res in results:
        if res['repliedAt'] is not None:
            res['repliedAt'] = res['repliedAt'].strftime("%Y-%m-%d %H:%M:%S")
        res['at'] = res['at'].strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        with open(finished_list_path, 'a+') as des:
            print(pkg_name, file=des)



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
                pkg_name = line.strip('\n')
                if pkg_name not in finished:
                    executor.submit(crawl_reviews, pkg_name=pkg_name,
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

    app_list_path = "data/vt_merged_year_2020_pkg_list.txt"
    finished_apps_path = "data/vt_finish.txt"
    save_path = "data/vt_reviews.txt"

    main(package_list_path=app_list_path, finished_list_path=finished_apps_path, save_file_path=save_path)
    # crawl_reviews(pkg_name="com.innovapps.diccionariodeanatomia", finished_list_path=finished_apps_path,
    #               save_path=save_path)