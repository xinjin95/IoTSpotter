#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_target_app.py
@time: 4/8/21 5:41 PM
@desc:
"""
import pandas as pd

df = pd.read_csv("/home/xin/Documents/code/python/iot-measure/data/final_dataset/package_label_list.csv")

sunil_list_path = "../data/androzoo/sunil_iot_pkgs.txt"
xin_list_path = "../data/androzoo/classification_result_iot_apps.txt"


def load_apps(file_path):
    apps = []
    with open(file_path, 'r') as file:
        for line in file:
            apps.append(line.strip('\n'))
    return apps


training_apps = list(df["app_id"])
sunil_apps = load_apps(sunil_list_path)
xin_apps = load_apps(xin_list_path)

all_apps = training_apps + sunil_apps + xin_apps
dids = set()
with open("../androzoo_download/data/app_list.txt", 'w+') as file:
    for app in all_apps:
        if app in dids:
            continue
        print(app, file=file)
        dids.add(app)