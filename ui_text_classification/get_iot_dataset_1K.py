#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_iot_dataset_1K.py
@time: 4/26/21 4:45 PM
@desc:
"""
import pandas as pd

xxx_path = "../data/ui_text_dataset/annotation/result/xxx_ui - xxx_ui.csv"
xxx_path = "../data/ui_text_dataset/annotation/result/ui-annoation - xxx.csv"

iot_apps = set()


def get_apps(file_path):
    df = pd.read_csv(file_path)
    if "Manual_label" in df.columns:
        labels = df["Manual_label"]
    else:
        labels = df["label"]
    pkg_names = df["pkg_name"]
    for i, pkg_name in enumerate(pkg_names):
        label = int(labels[i])
        if label == 1:
            iot_apps.add(pkg_name)


def record_apps():
    iot_path = "../data/ui_text_dataset/annotation/result/iot_app_list.txt"
    with open(iot_path, 'w+') as file:
        for app in iot_apps:
            print(app, file=file)


if __name__ == '__main__':
    get_apps(xxx_path)
    print(len(iot_apps))
    get_apps(xxx_path)
    print(len(iot_apps))
    record_apps()

