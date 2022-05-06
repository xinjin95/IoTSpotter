#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: static_lib_analysis.py
@time: 6/12/21 10:25 PM
@desc:
"""
import os
import pandas as pd
from execution import Executor

pkg_csv_path = "../app_url_collector/data/top_500_download_info.csv"


def collect_executable():
    cmd = "cp /home/xin/Documents/code/java/LibScope/out/artifacts/LibScope_jar/LibScope.jar jar_exe/LibScope.jar"
    os.system(cmd)
    cmd = "cp -avr /home/xin/Documents/code/java/LibScope/lib/ jar_exe/lib/"
    os.system(cmd)
    # cmd = "scp -r jar_exe/data/ zyueinfosec@pitzer.osc.edu:/users/PAS1888/zyueinfosec/xinjin/app_url_collector/jar_exe/"
    # os.system(cmd)
    # cmd = "scp jar_exe/linkScope.jar zyueinfosec@pitzer.osc.edu:/users/PAS1888/zyueinfosec/xinjin/app_url_collector/jar_exe/"
    # os.system(cmd)


def analyze_top_apps():
    exe = Executor(work_path="jar_exe/")
    # exe = Executor()
    df = pd.read_csv(pkg_csv_path)
    # adb = ADB(apk_path=apk_path, device=device)
    apk_path = "/home/xin/Documents/project/iot_measurement/apks"
    log_dir = "../data/lib_log/"
    out_put_dir = "../data/lib_results/"
    for i, pkg_name in enumerate(df["pkg_name"]):
        print("{}-th app: {}".format(i, pkg_name))
        # if i > 50:
        #     continue
        cmd = "java -jar LibScope.jar {}/{}.apk {} {}".format(apk_path, pkg_name, out_put_dir, log_dir)
        # cmd = "cp {}/{}.apk data/apks/".format("/home/xin/Documents/project/iot_measurement/apks/", pkg_name, pkg_name)
        exe.execute(cmd)


if __name__ == '__main__':
    # collect_executable()
    analyze_top_apps()