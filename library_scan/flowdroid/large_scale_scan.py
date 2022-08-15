#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: large_scale_scan.py
@time: 8/3/21 1:43 PM
@desc:
"""
import glob

import pandas as pd
from hashlib import sha256
from utility.execution import Executor
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# target_app_path = "data/target_apps.txt"
target_app_path = "/home/xxx/Documents/code/python/iot-measure/library_scan/flowdroid/data/target_apps.txt"
apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
app_download_log_path = "data/app_download_log.txt"
# app_download_log_path = "data/app_download_log.txt"
# app_download_log_path = "data/app_download_log.txt"
flowdroid_result_dir = "data/analysis_results/"
flowdroid_analysis_log_path = "data/flowdroid_analysis_log.txt"

lock = threading.Lock()
thread_num = 40
executor = ThreadPoolExecutor(max_workers=thread_num)


def get_app_list() -> list:
    result = list()
    with open(target_app_path, 'r') as file:
        for line in file:
            app_name = line.strip('\n')
            result.append(app_name)
    return result


def app_download_log(msg):
    with lock:
        with open(app_download_log_path, 'a+') as f:
            print(msg, file=f)


def flowdroid_analysis_log(msg):
    with lock:
        with open(flowdroid_analysis_log_path, 'a+') as f:
            print(msg, file=f)


def download_one_package(package_name):
    exe = Executor(work_path=apk_dir)
    cmd = "wget -q http://164.107.119.61:8881/st2/apks/xxxxxx.2021.04/%s.apk" % package_name
    exe.execute(cmd)
    app_path = apk_dir + package_name + ".apk"
    if os.path.exists(app_path):
        msg = "{},download success".format(package_name)
    else:
        msg = "{},download failure".format(package_name)
    app_download_log(msg)
    print(msg)


def download_all_apks():
    app_list = get_app_list()
    for i, app in enumerate(app_list):
        print(i, "-th, ", app)
        # download_one_package(app)
        executor.submit(download_one_package, package_name=app)
        while executor._work_queue.qsize() > thread_num:
            time.sleep(1)
    executor.shutdown(wait=True)


def analyze_one_app(package_name):
    flowdroid_jar_path = "/home/xxx/Downloads/flowdroid/soot-infoflow-cmd-2.8.0-jar-with-dependencies.jar"
    android_jar_path = "/home/xxx/Documents/code/android/android-platforms/android-30/android.jar"
    sink_file_path = "/home/xxx/Downloads/flowdroid/sources_and_sinks.txt"
    apk_file_path = apk_dir + package_name + ".apk"
    xml_result_path = flowdroid_result_dir + package_name + '.xml'
    cmd = "java -jar {} -p {} -s {} -a {} -o {}".format(flowdroid_jar_path,
                                                        android_jar_path,
                                                        sink_file_path,
                                                        apk_file_path,
                                                        xml_result_path)
    exe = Executor()
    exe.execute(cmd)
    if os.path.exists(xml_result_path):
        msg = "{},analysis success".format(package_name)
    else:
        msg = "{},analysis failure".format(package_name)
    flowdroid_analysis_log(msg)
    print(msg)


def download_failure_app():
    failed_apps = []
    with open("data/app_download_log.txt", 'r') as f:
        for line in f:
            pkg_name, msg = line.strip('\n').split(',')
            if msg == "download failure":
                failed_apps.append(pkg_name)
    print(f'# of failed apps: {len(failed_apps)}')
    failed_apps = set(failed_apps)
    df = pd.read_csv("../../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv")
    for i, pkg_name in enumerate(df["pkg_name"]):
        if pkg_name in failed_apps:
            sha = df["sha256"][i]
            exe = Executor(work_path=apk_dir)
            print("{}: download {}".format(os.getpid(), pkg_name))
            cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
                  " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
            # print(cmd)
            exe.execute(cmd)
            with open("%s/%s.apk" % (apk_dir, sha), 'rb') as file:
                data = file.read()
                sha256_returned = sha256(data).hexdigest()
                if sha256_returned.lower() == str(sha).lower():
                    cmd = "mv %s.apk %s.apk" % (sha, pkg_name)
                    msg = "{},{},{}".format(os.getpid(), pkg_name, "download success")
                else:
                    cmd = "rm %s.apk" % sha
                    # exe.execute(cmd)
                    msg = "{},{},{}".format(os.getpid(), pkg_name, "download failure")
            exe.execute(cmd)
            print(msg)

def analyze_all_apps():
    app_list = get_app_list()
    for i, app in enumerate(app_list):
        print(i, "-th, ", app)
        executor.submit(analyze_one_app, package_name=app)
        while executor._work_queue.qsize() > thread_num:
            time.sleep(1)
    executor.shutdown(wait=True)


def analyze_app_test():
    test_app = "de.twokit.castbrowser"
    analyze_one_app(test_app)


def download_rest_apps():
    finished = set(get_app_list())
    rest_num = 0
    with open("../../data/androzoo/description-improvement/xxx_xxx_shared_pkgs.txt", 'r') as f:
        for i, line in enumerate(f):
            app = line.strip('\n')

            if app in finished:
                print(i, "-th, ", "[-] finished:", app)
                continue
            print(i, "-th, ", app)
            rest_num +=1
            # download_one_package(app)
        #     executor.submit(download_one_package, package_name=app)
        #     while executor._work_queue.qsize() > thread_num:
        #         time.sleep(1)
        # executor.shutdown(wait=True)
    print(rest_num)


def download_other_apps():
    finished = set(get_app_list())
    total = 0 # 27020 - 26368 = 652
    df = pd.read_csv("../../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv")
    for i, pkg_name in enumerate(df["pkg_name"]):
        app_path = apk_dir + pkg_name + ".apk"
        if not os.path.exists(app_path) and pkg_name not in finished:
            total += 1
            # continue
            sha = df["sha256"][i]
            exe = Executor(work_path=apk_dir)
            print("{}: download {}".format(os.getpid(), pkg_name))
            cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
                  " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
            # print(cmd)
            exe.execute(cmd)
            with open("%s/%s.apk" % (apk_dir, sha), 'rb') as file:
                data = file.read()
                sha256_returned = sha256(data).hexdigest()
                if sha256_returned.lower() == str(sha).lower():
                    cmd = "mv %s.apk %s.apk" % (sha, pkg_name)
                    msg = "{},{},{}".format(os.getpid(), pkg_name, "download success")
                else:
                    cmd = "rm %s.apk" % sha
                    # exe.execute(cmd)
                    msg = "{},{},{}".format(os.getpid(), pkg_name, "download failure")
            exe.execute(cmd)
            print(msg)
    print(total)


def download_one_app_sha256(sha, pkg_name):
    exe = Executor(work_path=apk_dir)
    print("{}: download {}".format(os.getpid(), pkg_name))
    cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
          " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
    # print(cmd)
    exe.execute(cmd)
    with open("%s/%s.apk" % (apk_dir, sha), 'rb') as file:
        data = file.read()
        sha256_returned = sha256(data).hexdigest()
        if sha256_returned.lower() == str(sha).lower():
            cmd = "mv %s.apk %s.apk" % (sha, pkg_name)
            msg = "{},{}".format(pkg_name, "download success")
        else:
            cmd = "rm %s.apk" % sha
            # exe.execute(cmd)
            msg = "{},{}".format(pkg_name, "download failure")
    exe.execute(cmd)
    app_download_log(msg)


def download_lib_apps():
    target_apps = set(get_app_list())
    df = pd.read_csv("../../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv")
    for i, pkg_name in enumerate(df["pkg_name"]):
        app_path = apk_dir + pkg_name + ".apk"
        sha_str = df["sha256"][i]
        if not os.path.exists(app_path) and pkg_name in target_apps:
            executor.submit(download_one_app_sha256, sha=sha_str, pkg_name=pkg_name)
            while executor._work_queue.qsize() > thread_num:
                time.sleep(1)
    executor.shutdown(wait=True)


def split_apps_into_groups():
    root_dir = "/home/xxx/Documents/project/iot_measurement/iot_rest_apps/"
    files = glob.glob(root_dir + '*')
    for i, file in enumerate(files):
        dir_index = int(i / 2702)
        sub_dir = root_dir + '{}/'.format(dir_index)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        if not os.path.exists(sub_dir + os.path.basename(file)):
            os.rename(file, sub_dir + os.path.basename(file))


def inspect_split_res():
    root_dir = "/home/xxx/Documents/project/iot_measurement/iot_rest_apps/"
    files = glob.glob(root_dir + '*')
    # dir_name, dirs, filenames = next(os.walk(root_dir))
    # print('')
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
                apk_num += 1
    print(apk_num)


def collect_iot_app_not_in_nas():
    failed_apps = []
    with open("data/app_download_log.txt", 'r') as f:
        for line in f:
            pkg_name, msg = line.strip('\n').split(',')
            if msg == "download failure":
                failed_apps.append(pkg_name)

    for app in failed_apps:
        with open("data/iot_app_not_in_nas.txt", 'a+') as f:
            print(app, file=f)


def remove_failed_apps():
    files = glob.glob(apk_dir+'*')
    apps = set(get_app_list())
    for file in files:
        if not file.endswith('.apk'):
            continue
        apk_name = os.path.basename(file)[:-4]
        # print(file, apk_name)
        if apk_name not in apps:
            print(file, apk_name)

if __name__ == '__main__':
    # download_all_apks()
    # download_failure_app()
    # analyze_app_test()
    # analyze_all_apps()
    # download_rest_apps()
    # download_other_apps()
    # split_apps_into_groups()
    # inspect_split_res()
    # collect_iot_app_not_in_nas()
    # download_lib_apps()
    remove_failed_apps()