#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: download_error_check.py
@time: 6/15/21 9:22 AM
@desc:
"""
import os
from utility.execution import Executor
from hashlib import sha256

package_dir = "data/apks"


def download_one_package(package_name, sha):
    global msg
    if os.path.isfile("%s/%s.apk" % (package_dir, package_name)):
        msg = "{},{},{}".format(os.getpid(), package_name, "download success")
        print(msg)
        return True
    exe = Executor(work_path=package_dir)
    print("{}: download {}".format(os.getpid(), package_name))
    cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
          " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
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


if __name__ == '__main__':
    pkg_name, sha_name = "app.homey", "F742085FF9B67834B8E814835F0031F8B097E8A62FB654D4BF3E9DF677753E2E"
    download_one_package(pkg_name, sha_name)