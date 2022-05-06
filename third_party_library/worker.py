#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: worker.py
@time: 6/12/21 11:42 PM
@desc:
"""
from multiprocessing.managers import BaseManager
import pandas as pd
import os
from execution import Executor
from hashlib import sha256
import traceback

global msg
# package_dir = "/users/PAS1888/zyueinfosec/xinjin/third_party_library/data/apks"
package_dir = "data/apks"

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


def download_one_package(package_name, sha):
    global msg
    if os.path.isfile("%s/%s.apk" % (package_dir, package_name)):
        msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        print(msg)
        return True
    exe = Executor(work_path=package_dir)
    print("{}: download {}".format(os.getpid(), package_name))
    # cmd = "curl --silent -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
    #       " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
    cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
          " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
    print(cmd)
    exe.execute(cmd)
    with open("%s/%s.apk" % (package_dir, sha), 'rb') as file:
        data = file.read()
        sha256_returned = sha256(data).hexdigest()
        if sha256_returned.lower() == str(sha).lower():
            cmd = "mv %s.apk %s.apk" % (sha, package_name)
            msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        else:
            cmd = "rm %s.apk" % sha
            # exe.execute(cmd)
            msg = "{},{},{}".format(os.getpid(), package_name, "download failure")
    exe.execute(cmd)
    if os.path.isfile("%s/%s.apk" % (package_dir, package_name)):
        msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        print(msg)
        return True
    else:
        msg = "{},{},{}".format(os.getpid(), package_name, "download failure")
        print(msg)
        return False


def analyze_one_app(apk_path, pkg_name):
    global msg
    # out_put_dir = "/users/PAS1888/zyueinfosec/xinjin/third_party_library/data/2M_lib_results/"
    out_put_dir = "data/2M_lib_results/"
    # log_dir = "/users/PAS1888/zyueinfosec/xinjin/third_party_library/data/2M_lib_log/"
    log_dir = "data/2M_lib_log/"
    # exe = Executor(work_path="/users/PAS1888/zyueinfosec/xinjin/third_party_library/jar_exe/")
    exe = Executor(work_path="jar_exe/")
    cmd = "java -jar LibScope.jar {} {} {}".format(apk_path,  out_put_dir, log_dir)
    exe.execute(cmd)
    msg = "{},{},{}".format(os.getpid(), pkg_name, "static analysis success")


def main():
    global msg
    # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # 连接到服务器，也就是运行task_master.py的机器:
    # server_addr = 'pitzer-login04'
    server_addr = "127.0.0.1"

    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 5100), authkey=b'abc')

    # 从网络连接:
    m.connect()
    # 获取Queue的对象:
    task = m.get_task_queue()
    result = m.get_result_queue()

    # app_csv_path = "data/xin_sunil_shared_sha256_androzoo.csv"
    # df = pd.read_csv(app_csv_path)

    while True:
        try:
            task_msg = task.get(timeout=10)
            task_list = task_msg.split(',')
            print("task list:", task_list)
            if len(task_list) != 3:
                msg = "{},{},{}".format(os.getpid(), "no_pkg_name", task_msg.replace(',', '/'))
            else:
                pkg_name, sha = task_list[1], task_list[2]
                print("{},get task: {}".format(os.getpid(), pkg_name))
                apk_path = "%s/%s.apk" % (package_dir, pkg_name)
                if download_one_package(pkg_name, sha):
                    # apk_path = "%s/%s.apk" % (package_dir, pkg_name)
                    analyze_one_app(apk_path, pkg_name)
                if os.path.isfile(apk_path):
                    os.remove(apk_path)
                sha_apk_path = "%s/%s.apk" % (package_dir, sha)
                if os.path.isfile(sha_apk_path):
                    os.remove(sha_apk_path)
                print(msg)
            # if index == len(df):
            #     print("df len equals")
            #     break
            # pkg_name, sha = df['pkg_name'][index], df['sha256'][index]
            result.put(msg)
        except:
            print(traceback.format_exc())
            break


if __name__ == '__main__':
    main()