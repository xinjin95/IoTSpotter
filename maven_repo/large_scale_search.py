#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: large_scale_search.py
@time: 6/27/21 11:21 PM
@desc:
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, json
import threading
import pandas as pd
import requests
import os
import argparse

lock = threading.Lock()
thread_num = 10
executor = ThreadPoolExecutor(max_workers=thread_num)

lib_freq_path = "data/lib_frequency.csv"
search_result_path = "data/search_result.txt"
package_queue = list()


def search_package_name(package_name):
    url = 'https://search.maven.org/solrsearch/select?q=fc:"{}"&rows=20&wt=json'.format(package_name)
    resp = requests.get(url)
    print("search for: ", package_name, resp.status_code)
    if resp.status_code == 429:
        package_queue.append(package_name)
        time.sleep(5)
        return
    elif resp.status_code == 403:
        package_queue.append(package_name)
        time.sleep(60)
        return
    result_json = resp.content.decode("utf-8")
    with lock:
        with open(search_result_path, 'a+') as file:
            print(package_name + ":" +  result_json, file=file)
    time.sleep(1)


def get_finished() -> set:
    finished = set()
    if not os.path.isfile(search_result_path):
        print("Search result file not exist!")
        return finished
    with open(search_result_path, 'r') as file:
        for line in file:
            pkg_name, _ = line.split(':', 1)
            finished.add(pkg_name)
    return finished


def main(left_index, right_index):
    df = pd.read_csv(lib_freq_path)
    finished = get_finished()
    print("Total num of finished:", len(finished))
    with open(lib_freq_path, 'r') as src:
        for i, pkg_name in enumerate(df["package_name"]):
            # print("{}-th, {}".format(i, pkg_name))
            if left_index <= i <= right_index:
                if pkg_name not in finished:
                    package_queue.append(pkg_name)
                else:
                    print("[*] did " + pkg_name)
    while len(package_queue) != 0:
        print("Rest # of packages:", len(package_queue))
        executor.submit(search_package_name, package_queue.pop())
        while executor._work_queue.qsize() > thread_num:
            time.sleep(1)
    executor.shutdown(wait=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--left", type=int, required=True)
    parser.add_argument("-r", "--right", type=int, required=True)
    args = parser.parse_args()
    main(args.left, args.right)
    # main(0, 6000)