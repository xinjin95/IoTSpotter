#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: parse_apks.py
@time: 8/17/21 3:22 PM
@desc:
"""
import json
import os
import glob

import threading
from concurrent.futures import ThreadPoolExecutor
import time
from library_scan.flowdroid.large_scale_scan import get_app_list, download_one_package


jar_path = "data/manifest_parser_jar/manifestParser.jar"
result_dir = "data/manifest_parse_result"
log_path = "data/manifest_parser_log.txt"
thread_num = 20
executor = ThreadPoolExecutor(max_workers=thread_num)
lock = threading.Lock()


def get_latest_jar():
    jar_src_path = "/home/xxx/Documents/code/java/manifestParser/out/artifacts/manifestParser_jar/manifestParser.jar"
    cmd = "cp {} {}".format(jar_src_path, jar_path)
    os.system(cmd)


def parse_one_apk(apk_path):
    cmd = "java -jar {} {} {} {}".format(jar_path,
                                         apk_path,
                                         result_dir,
                                         log_path)
    os.system(cmd)


def parse_test():
    # apk_path = "/home/xxx/Documents/project/iot_measurement/apks/com.alarmnet.tc2.apk"
    # parse_one_apk(apk_path)
    package_name = "com.redison.senstrokeupdater"
    download_parse_one_app(package_name)


def parse_local_apps():
    root_dir = "/home/xxx/Documents/project/iot_measurement/iot_rest_apps/"
    files = glob.glob(root_dir + '*')
    apk_num = 0
    while len(files) > 0:
        file = files.pop()
        if os.path.isdir(file):
            print(file)
            if not file.endswith('/'):
                file = file + '/'
            new_files = glob.glob(file + '*')
            files = files + new_files
        else:
            if file.endswith('.apk'):
                # parse_one_apk(file)
                executor.submit(parse_one_apk, apk_path=file)
                while executor._work_queue.qsize() > thread_num:
                    time.sleep(1)
                apk_num += 1
                print("Cur:", apk_num)
    print(apk_num)
    executor.shutdown(wait=True)


def download_parse_one_app(package_name):
    download_one_package(package_name)
    apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
    apk_path = apk_dir + package_name + '.apk'
    if os.path.exists(apk_path):
        get_apk_size(apk_path, package_name)
        parse_one_apk(apk_path)
        print("[*] success:", package_name)
        os.remove(apk_path)
    else:
        print("[-] No such file:", apk_path)


def parse_nas_apps():
    apps = get_app_list()
    for i, app in enumerate(apps):
        print("{}-th: {}".format(i, app))
        executor.submit(download_parse_one_app, package_name=app)
        while executor._work_queue.qsize() > thread_num:
            time.sleep(1)
    executor.shutdown(wait=True)


def get_apk_size(apk_path, app_name):
    res = os.path.getsize(apk_path)
    with lock:
        with open("data/apk_size.txt", 'a+') as f:
            print(json.dumps({"package_name": app_name, "size": res}), file=f)


def collect_app_size():
    root_dir = "/home/xxx/Documents/project/iot_measurement/iot_rest_apps/"
    files = glob.glob(root_dir + '*')
    apk_num = 0
    while len(files) > 0:
        file = files.pop()
        if os.path.isdir(file):
            print(file)
            if not file.endswith('/'):
                file = file + '/'
            new_files = glob.glob(file + '*')
            files = files + new_files
        else:
            if file.endswith('.apk'):
                apk_path = file
                package_name = os.path.basename(apk_path)
                package_name = package_name.replace('.apk', '')
                get_apk_size(apk_path, package_name)


if __name__ == '__main__':
    # get_latest_jar()
    # parse_test()
    # parse_local_apps()
    # parse_nas_apps()
    # parse_nas_apps()
    collect_app_size()