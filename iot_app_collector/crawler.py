#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: crawler.py
@time: 1/14/21 8:59 PM
@desc:
"""

import play_scraper
import _thread
import time
import json

success_result = []
success_packages = []
failed_packages = []
thread_ids = list(range(0, 4))
num_threads = len(thread_ids)


def crawler(package_name, thread_id):
    print("thread-{} for {}".format(thread_id, package_name))
    try:
        detail = play_scraper.details(package_name)
        detail['description_html'] = detail['description_html'].decode("utf-8")
        success_result.append(detail)
        success_packages.append(package_name)
    except:
        failed_packages.append(package_name)
    thread_ids.append(thread_id)
    # return detail
    # result = play_scraper.search(package_name, page=10)
    # if len(result) == 0:
    #     failed_packages.append("{},{}".format(package_name, "no search result"))
    # else:
    #     package_found = False
    #     for res in result:
    #         id = res['app_id']
    #         if id == package_name:
    #             package_found = True
    #             break
    #     if package_found:
    #         detail = play_scraper.details(package_name)
    #         success_result.append(detail)
    #         success_packages.append(package_name)
    #     else:
    #         failed_packages.append("{},{}".format(package_name, "search lib_results don't match"))
    # thread_ids.append(thread_id)
    # id = result[0]['app_id']
    # detail = play_scraper.details(id)
    # if package_name != detail['app_id']:
    #     print("{} and {} mis-match".format(package_name, detail['app_id']))
    #     failed_packages.append(package_name)
    # success_result.append(detail)
    # success_packages.append(package_name)


def get_package_list(file_path):
    return open(file_path, 'r').read().strip().split('\n')


def record_result(file_path, result_list, is_dict=False):
    with open(file_path, 'w+') as file:
        for result in result_list:
            if is_dict:
                file.write(json.dumps(result))
            else:
                file.write(result)
            file.write('\n')


def write_to_file():
    time.sleep(10)
    path_success_apps = "../data/package/app_download/metadata_iot_apps.txt"
    while len(success_result) != 0:
        with open(path_success_apps, 'a+') as file:
            res = success_result.pop()
            file.write(json.dumps(res))
            file.write('\n')


def main():
    seed_list = "../data/package/iot_package_available.txt"
    apps = get_package_list(seed_list)
    # apps = apps[0:100]
    # _thread.start_new_thread(write_to_file, ())
    for i, app in enumerate(apps):
        print("download {}-th app: {}".format(i, app))
        while len(thread_ids) == 0:
            time.sleep(0.1)
        _thread.start_new_thread(crawler, (app, thread_ids.pop()))

    while len(thread_ids) != num_threads:
        print("stuck in wait for finish {} - {}".format(num_threads, len(thread_ids)))
        time.sleep(1)
    path_success_apps = "../data/package/app_download/success_download_list.txt"
    record_result(path_success_apps, success_packages, is_dict=False)
    path_failed_apps = "../data/package/app_download/failed_download_list.txt"
    record_result(path_failed_apps, failed_packages, is_dict=False)
    path_result = "../data/package/app_download/metadata_iot_apps.txt"
    record_result(path_result, success_result, is_dict=True)


def check_task_finished():
    res = set([])
    with open("../data/package/app_download/metadata_iot_apps.txt", 'r') as file:
        for line in file:
            detail = json.loads(line)
            res.add(detail["app_id"])
    seed_list = "../data/package/iot_package_available.txt"
    apps = get_package_list(seed_list)
    apps = set(apps)
    print(len(res))
    print(len(apps))
    print(apps==res)


# def direct_download():
#     seed_list = "../data/package/iot_package_available.txt"
#     apps = get_package_list(seed_list)
#     file = open("../data/package/app_download/metadata_iot_apps.txt", 'a+')
#     for i, app in enumerate(apps):
#         detail = crawler(app, 0)
#         detail['description_html'] = detail['description_html'].decode("utf-8")
#         print(json.dumps(detail), file=file)

def test_non_existing(pkg_name):
    try:
        detail = play_scraper.details(pkg_name)
        detail['description_html'] = detail['description_html'].decode("utf-8")
    except Exception as e:
        # print(getattr(e, 'msg', e))
        print(e)

if __name__ == '__main__':
    test_non_existing("a.b.c")
    # check_task_finished()
    # direct_download()
    # main()
    # package_name = "huedynamic.android"
    # detail = play_scraper.details(package_name)
    # print(detail)
# apps = ['1', '2', '3']
# record_result("../data/iot-app/tmp.txt", apps)
# app = "com.linkedin.android"
#
# print(app)
#
# id = play_scraper.search(app, page=1)[0]['app_id']
#
# detail = play_scraper.details(id)
#
# url = detail['url']
#
# print(url)
#
# print(detail['description'])
