#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_dataset_ratio.py
@time: 4/24/21 4:30 PM
@desc:
"""
import pandas as pd

save_dir = "../data/dataset_ratio/"
training_path = "../data/final_dataset/package_label_list.csv"
above_3_path = "../data/iot_annotation/above_3.txt"

csv = pd.read_csv(training_path)

iot_apps = set()
non_iot_apps = set()

for i, pkg_name in enumerate(csv["app_id"]):
    label = int(csv["label"][i])
    if label == 0:
        non_iot_apps.add(pkg_name)
    elif label == 1:
        iot_apps.add(pkg_name)

above_3_apps = set()
with open(above_3_path, 'r') as file:
    for line in file:
        pkg_name, _ = line.split(',', 1)
        above_3_apps.add(pkg_name)

print(len(iot_apps))
print(len(non_iot_apps))
print(len(iot_apps.intersection(above_3_apps)))
print(len(iot_apps.difference(above_3_apps)))