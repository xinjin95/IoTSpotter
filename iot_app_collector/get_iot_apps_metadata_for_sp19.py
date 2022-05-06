#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_iot_apps_metadata_for_sp19.py
@time: 3/5/21 1:19 PM
@desc:
"""
import json

package_list_path = "../../data/dataset/iot_app_list.txt"
metadata_path = "../../data/androzoo/app_metadata.json"
save_path = "../../data/dataset/iot_app_metadata_sp19.txt"

iot_apps = open(package_list_path, 'r').read().strip().split('\n')
iot_apps = set(iot_apps)

print("iot apps set: {}".format(len(iot_apps)))

total = 0
with open(save_path, 'w+') as des:
    with open(metadata_path, 'r') as src:
        while True:
            lines = src.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for i, line in enumerate(lines):
                pkg_name, content = line.split(":", 1)
                if pkg_name not in iot_apps:
                    continue
                total += 1
                print("find: {}, {}".format(total, pkg_name))
                js = json.loads(content)
                print(json.dumps(js), file=des)
                iot_apps.remove(pkg_name)