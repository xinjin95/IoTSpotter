#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: identify_non_iot_apps_from_initial_iot_set.py
@time: 4/27/21 11:47 AM
@desc:
"""

import pandas as pd

df = pd.read_csv("../data/final_dataset/package_label_list.csv")

iot_apps = set()
non_iot_apps = set()

for i, pkg_name in enumerate(df["app_id"]):
    label = df["label"][i]
    label = int(label)
    if label == 1:
        iot_apps.add(pkg_name)
    elif label == 0:
        non_iot_apps.add(pkg_name)

sp_19_apps = open("../data/sp19_dataset/app_list.txt").read().strip().split('\n')
sp_19_apps = set(sp_19_apps)

above_3_apps = set()
with open("../data/iot_annotation/above_3.txt", 'r') as file:
    for line in file:
        pkg_name, _ = line.split(',', 1)
        above_3_apps.add(pkg_name)

print(len(non_iot_apps.intersection(sp_19_apps)))
print(len(non_iot_apps.intersection(above_3_apps)))