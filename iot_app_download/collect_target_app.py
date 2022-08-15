#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: collect_target_app.py
@time: 4/8/21 5:41 PM
@desc:
"""
import pandas as pd

df = pd.read_csv("/home/xxx/Documents/code/python/iot-measure/data/final_dataset/package_label_list.csv")

xxx_list_path = "../data/androzoo/xxx_iot_pkgs.txt"
xxx_list_path = "../data/androzoo/classification_result_iot_apps.txt"


def load_apps(file_path):
    apps = []
    with open(file_path, 'r') as file:
        for line in file:
            apps.append(line.strip('\n'))
    return apps


training_apps = list(df["app_id"])
xxx_apps = load_apps(xxx_list_path)
xxx_apps = load_apps(xxx_list_path)

all_apps = training_apps + xxx_apps + xxx_apps
dids = set()
with open("../androzoo_download/data/app_list.txt", 'w+') as file:
    for app in all_apps:
        if app in dids:
            continue
        print(app, file=file)
        dids.add(app)