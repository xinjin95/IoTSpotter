#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: large_scale_crawler.py
@time: 1/25/21 9:54 PM
@desc:
"""
import os.path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, json
import traceback
import threading
import play_scraper

# codes = ['us', 'lu', 'fr', 'ca']
codes = ['lu', 'fr', 'ca']
# country_code = codes[0]

lock = threading.Lock()
thread_num = 40
executor = ThreadPoolExecutor(max_workers=thread_num)


# pkg_name_path = "../data/androzoo/gplay_pkg_name.txt"
pkg_name_path = "../data/androzoo/description-improvement/xin_sunil_shared_pkgs.txt"


# test_apps = []


def get_details(pkg_name, country_code):
    # test_apps.append(pkg_name)
    try:
        detail = play_scraper.details(pkg_name, gl=country_code)
        detail['description_html'] = detail['description_html'].decode("utf-8")
        detail = json.dumps(detail)
        print(pkg_name+":"+detail)
        with lock:
            metadata_path = f"../data/androzoo/geo_difference/{country_code}_metadata.json"
            with open(metadata_path, 'a+') as file:
                file.write(pkg_name+ ":" + detail + "\n")
        return
    except Exception as e:
        print(pkg_name + ":" + str(e))
        with lock:
            error_path = f"../data/androzoo/geo_difference/{country_code}_error.txt"
            with open(error_path, 'a+') as file:
                file.write(pkg_name + ":" + str(e) + "\n")
        return


def get_finish_list(country_code) -> set:
    dids = set()
    metadata_path = f"../data/androzoo/geo_difference/{country_code}_metadata.json"
    if not os.path.exists(metadata_path):
        return dids
    total = 0
    print("finished list reading")
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines()
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, _ = line.split(":", 1)
                    # print(line)
                    dids.add(pkg_name)
                    total += 1
                    print(total)
                except:
                    print(line)
                    # exit(1)
    metadata_num = len(dids)
    print("error reading")
    error_path = f"../data/androzoo/geo_difference/{country_code}_error.txt"
    with open(error_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, msg = line.split(":", 1)
                    if "Invalid application ID" in msg:
                        dids.add(pkg_name)
                        total += 1
                        print(total)
                except:
                    print(line)
                    # exit(1)
    error_num = len(dids) - metadata_num
    print("metadata #: {}".format(metadata_num))
    print("error #: {}".format(error_num))
    print("total #: {}".format(total))
    return dids


def main(country_code):
    finished = get_finish_list(country_code)
    print("finished: {}".format(len(finished)))
    with open(pkg_name_path, 'r') as file:
        while True:
            # if len(test_apps) > 10000:
            #     break
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                pkg_name = line.strip('\n')
                if pkg_name not in finished:
                    executor.submit(get_details, pkg_name=pkg_name, country_code=country_code)
                    while executor._work_queue.qsize() > thread_num:
                        time.sleep(1)
                else:
                    print("[*] did " + pkg_name)
    # executor.shutdown(wait=True)


def read_json(country_code=codes[0]):
    metadata_path = f"../data/androzoo/geo_difference/{country_code}_metadata.json"
    with open(metadata_path, 'r') as file:
        for line in file:
            pkg_name, data = line.split(":", 1)
            js = json.loads(data)
            print(js)


if __name__ == '__main__':
    # get_details("com.linkedin.android")
    # read_json()
    # start_time = time.time()
    for c_code in codes:
        main(c_code)
    executor.shutdown(wait=True)
    # main(codes[3])
    # get_finish_list()
    # print(time.time()-start_time)