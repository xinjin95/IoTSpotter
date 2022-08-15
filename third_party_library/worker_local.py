#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: worker_local.py
@time: 7/12/21 3:30 PM
@desc:
"""
from multiprocessing.managers import BaseManager
import pandas as pd
import os
from execution import Executor
from hashlib import sha256
import traceback

global msg
# package_dir = "/users/PAS1888/zyueinfosec/xxxxxx/third_party_library/data/apks"
package_dir = "data/apks"


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


def download_one_package(package_name):
    global msg
    if os.path.isfile("%s/%s.apk" % (package_dir, package_name)):
        msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        print(msg)
        return True
    exe = Executor(work_path=package_dir)
    print("{}: download {}".format(os.getpid(), package_name))
    cmd = "wget http://164.107.119.61:8881/st3/apks/2020.06/%s.apk" % package_name
    exe.execute(cmd)
    if os.path.isfile("%s/%s.apk" % (package_dir, package_name)):
        msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        print(msg)
        return True
    else:
        msg = "{},{},{}".format(os.getpid(), package_name, "download failure")
        print(msg)
        return False


def analyze_one_app(pkg_name):
    global msg
    # out_put_dir = "/users/PAS1888/zyueinfosec/xxxxxx/third_party_library/data/2M_lib_results/"
    out_put_dir = os.getcwd() + "/data/2M_lib_results/"
    # log_dir = "/users/PAS1888/zyueinfosec/xxxxxx/third_party_library/data/2M_lib_log/"
    log_dir = os.getcwd() + "/data/2M_lib_log/"
    apk_path = os.getcwd() + "/data/apks/{}.apk".format(pkg_name)
    # exe = Executor(work_path="/users/PAS1888/zyueinfosec/xxxxxx/third_party_library/jar_exe/")
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
    server_addr = "164.107.119.54"

    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 5100), authkey=b'abc')

    # 从网络连接:
    m.connect()
    # 获取Queue的对象:
    task = m.get_task_queue()
    result = m.get_result_queue()

    while True:
        try:
            task_msg = task.get(timeout=10)
            task_list = task_msg.split(',')
            print("task list:", task_list)
            if len(task_list) != 2:
                msg = "{},{}".format(os.getpid(), "no_pkg_name", task_msg.replace(',', '/'))
            else:
                pkg_name = task_list[1]
                print("{},get task: {}".format(os.getpid(), pkg_name))
                apk_path = "%s/%s.apk" % (package_dir, pkg_name)
                if download_one_package(pkg_name):
                    # apk_path = "%s/%s.apk" % (package_dir, pkg_name)
                    analyze_one_app(pkg_name)
                if os.path.isfile(apk_path):
                    os.remove(apk_path)
                print(msg)
            result.put(msg)
        except:
            print(traceback.format_exc())
            break


if __name__ == '__main__':
    main()