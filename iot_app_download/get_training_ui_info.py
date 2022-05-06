#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_training_ui_info.py
@time: 4/9/21 3:57 PM
@desc:
"""
import pandas as pd
import os

csv_path = "data/package_label_list.csv"

df = pd.read_csv(csv_path)

iot_apps = set()
non_iot_apps = set()

for i, app in enumerate(df["app_id"]):
    label = df["label"][i]
    label = int(label)
    if label == 0:
        non_iot_apps.add(app)
    elif label == 1:
        iot_apps.add(app)

target_apps = iot_apps.union(non_iot_apps)


# os.mkdir("data/test_ui_info/")
# os.mkdir("data/training_ui_info/iot/")
# os.mkdir("data/training_ui_info/non_iot/")
did = set()
total = 0
dirpath, dirnames, filenames = next(os.walk("data/ui_info/"))
for file in filenames:
    pkg_name = file.replace('_ui_info.txt', '')
    cmd = ""
    if pkg_name in did:
        continue
    did.add(pkg_name)
    if pkg_name not in target_apps:
        total += 1
        print(total)
        # cmd = "cp data/ui_info/{} data/test_ui_info/".format(file)
    # elif pkg_name in non_iot_apps:
    #     cmd = "cp data/ui_info/{} data/training_ui_info/non_iot/".format(file)
    # if cmd != "":
    #     os.system(cmd)