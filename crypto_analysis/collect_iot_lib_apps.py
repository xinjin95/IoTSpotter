#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_iot_lib_apps.py
@time: 12/14/21 10:38 PM
@desc:
"""
import json
import os.path

apk_dir = "/home/xin/Documents/project/iot_measurement/iot_lib_apps/"

def get_lib_apps():
    iot_lib_app_path = "data/call_graph_analysis/iot_lib_apps.txt"
    src_path = "cryptoguard_results/cryptoguard_flaws.txt"
    with open(iot_lib_app_path, 'a+') as des:
        with open(src_path, 'r') as f:
            for line in f:
                js = json.loads(line)
                pkg_name = js["app_name"]
                if os.path.isfile(apk_dir + pkg_name + '.apk'):
                    print(pkg_name, file=des)


def cryptoguard():
    src_path = "cryptoguard_results/cryptoguard_flaws.txt"
    with open(src_path, 'r') as f:
        for line in f:
            js = json.loads(line)


# get_lib_apps()