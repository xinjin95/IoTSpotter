#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: worker.py
@time: 8/4/21 10:35 AM
@desc:
"""
from multiprocessing.managers import BaseManager
import pandas as pd
import os
from execution import Executor
from hashlib import sha256
import traceback

global msg

package_dir = "data/apks"
flowdroid_result_dir = "data/analysis_results/"

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


def analyze_one_app(package_name):
    global msg
    flowdroid_jar_path = "jar_exe/soot-infoflow-cmd-2.8.0-jar-with-dependencies.jar"
    android_jar_path = "jar_exe/android-30.jar"
    sink_file_path = "jar_exe/sources_and_sinks.txt"
    apk_file_path = "%s/%s.apk" % (package_dir, package_name)

    xml_result_path = flowdroid_result_dir + package_name + '.xml'
    cmd = "java -jar {} -p {} -s {} -a {} -o {} -ct 300 -dt 300 -rt 300 ".format(flowdroid_jar_path,
                                                        android_jar_path,
                                                        sink_file_path,
                                                        apk_file_path,
                                                        xml_result_path)
    exe = Executor()
    exe.execute(cmd)
    if os.path.exists(xml_result_path):
        msg = "{},{},{}".format(os.getpid(), package_name, "scan success")
    else:
        msg = "{},{},{}".format(os.getpid(), package_name, "scan failure")
    # flowdroid_analysis_log(msg)
    # print(msg)


def main():
    global msg

    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # server_addr = 'pitzer-login04'
    server_addr = "192.148.247.179"

    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 7100), authkey=b'abc')

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
            if len(task_list) != 3:
                msg = "{},{},{}".format(os.getpid(), "no_pkg_name", task_msg.replace(',', '/'))
            else:
                pkg_name, sha = task_list[1], task_list[2]
                print("{},get task: {}".format(os.getpid(), pkg_name))
                apk_path = "%s/%s.apk" % (package_dir, pkg_name)
                if download_one_package(pkg_name, sha):
                    analyze_one_app(pkg_name)
                if os.path.isfile(apk_path):
                    os.remove(apk_path)
                sha_apk_path = "%s/%s.apk" % (package_dir, sha)
                if os.path.isfile(sha_apk_path):
                    os.remove(sha_apk_path)
                print(msg)
            result.put(msg)
        except:
            print(traceback.format_exc())
            break


if __name__ == '__main__':
    main()