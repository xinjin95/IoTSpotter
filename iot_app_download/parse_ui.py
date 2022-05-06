#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: parse_ui.py
@time: 4/9/21 1:13 PM
@desc:
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import argparse
import os


apk_path = "/home/xin/Documents/iot_app_download/data/apk/"
ui_info_path = "/home/xin/Documents/iot_app_download/data/ui_info/"
jar_path = "/home/xin/Documents/iot_app_download/data/parser/LayoutAnalyzer.jar"
jar_dependency_path = "/home/xin/Documents/iot_app_download/data/parser/"
log_path = "/home/xin/Documents/iot_app_download/data/parse_log.txt"
lock = threading.Lock()
thread_num = 5
executor = ThreadPoolExecutor(max_workers=thread_num)


def execute(cmd, cwd=apk_path):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd=cwd)
    process.wait()


def download_app(pkg_name):
    cmd = "wget -q http://164.107.119.61:8881/st2/apks/JinXin.2021.04/{}.apk".format(pkg_name)
    execute(cmd, cwd=apk_path)


def parse_app(pkg_name):
    cmd = "java -jar {} {} {} {}".format(jar_path, apk_path + pkg_name + ".apk", ui_info_path, log_path)
    execute(cmd, cwd=jar_dependency_path)


def process_single_app(pkg_name, finish_path):
    download_app(pkg_name)
    print("[-] download: ", pkg_name)
    parse_app(pkg_name)
    print("[-] parse: ", pkg_name)
    try:
        os.remove(apk_path + pkg_name + ".apk")
        print("[-] remove:", pkg_name)
        with lock:
            with open(finish_path, 'a+') as des:
                print(pkg_name, file=des)
    except:
        print("[-] remove failed:", pkg_name)


def get_finish_list(finish_path):
    finished = set()
    with open(finish_path, 'r') as file:
        for line in file:
            pkg_name = line.strip('\n')
            finished.add(pkg_name)
    return finished


def main(pkg_path, finished_path):
    finished = get_finish_list(finished_path)
    print("finished: {}".format(len(finished)))
    with open(pkg_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                pkg_name = line.strip('\n')
                if pkg_name not in finished:
                    executor.submit(process_single_app, pkg_name=pkg_name, finish_path=finished_path)
                    while executor._work_queue.qsize() > thread_num:
                        time.sleep(1)
                else:
                    print("[*] did " + pkg_name)
    executor.shutdown(wait=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pkg_list_path", type=str, required=True)
    parser.add_argument("-f", "--finish_list_path", type=str, required=True)

    args = parser.parse_args()

    app_list_path = args.pkg_list_path
    finished_list_path = args.finish_list_path

    main(pkg_path=app_list_path, finished_path=finished_list_path)
