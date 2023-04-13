#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: download.py
@time: 4/8/21 5:55 PM
@desc:
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import os
import hashlib

csv_file_path = "data/app_download_info.csv"
finished_path = "data/finished.txt"
error_path = "data/error.txt"
lock = threading.Lock()
thread_num = 30
executor = ThreadPoolExecutor(max_workers=thread_num)
lock_error = threading.Lock()
apk_path = "/storage2/apks/xxxxxx.2021.04/"
# apk_path = "data/"


# def execute(cmd, cwd="/storage2/apks/xxxxxx.2021.04/"):
def execute(cmd, cwd=apk_path):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd=cwd)
    process.wait()


def get_finished():
    finished = set([])
    with open('data/finished.txt', 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            if line != "":
                finished.add(line)
    return finished


def check_sha256(pkg_name, sha256):
    print("check sha256")
    hash_res = ""
    with open("{}{}.apk".format(apk_path, sha256), 'rb') as f:
        bytes = f.read()
        hash_res = hashlib.sha256(bytes).hexdigest()
    print(hash_res)
    if str(sha256).lower() == hash_res:
        print("[-] sha256 match:", pkg_name, sha256)
        try:
            os.rename("{}{}.apk".format(apk_path, sha256), "{}{}.apk".format(apk_path, pkg_name))
        except:
            with lock_error:
                with open(error_path, 'a+') as des:
                    print(pkg_name, file=des)
    else:
        print("[-] sha256 NOT match:", pkg_name, sha256)
        os.remove("{}{}.apk".format(apk_path, sha256))
        with lock_error:
            with open(error_path, 'a+') as des:
                print(pkg_name, file=des)


def single_download(pkg_name, sha256):
    cmd = "curl -s -O --remote-header-name -G -d apikey=your_api_key" \
          " -d sha256=%s https://androzoo.uni.lu/api/download" % sha256 # put replace your_api_key with your own Androzoo key.
    execute(cmd)
    check_sha256(pkg_name, sha256)
    with lock:
        with open(finished_path, 'a+') as file:
            print(pkg_name, file=file)
    print("[-] download:", pkg_name, sha256)


def main():
    finished = get_finished()
    print("finished: {}".format(len(finished)))
    with open(csv_file_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                pkg_name, sha256, _ = line.split(',')
                if pkg_name not in finished:
                    executor.submit(single_download, pkg_name=pkg_name, sha256=sha256)
                    while executor._work_queue.qsize() > thread_num:
                        time.sleep(1)
                else:
                    print("[*] did " + pkg_name)
    executor.shutdown(wait=True)


if __name__ == '__main__':
    main()
