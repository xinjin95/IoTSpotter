#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_apps_for_ui_parsing.py
@time: 4/19/21 4:04 PM
@desc:
"""
import pandas as pd

training_csv_path = "../data/final_dataset/package_label_list.csv"
save_path = "../data/final_dataset/training_set_list.txt"

df = pd.read_csv(training_csv_path)
file_save = open(save_path, 'a+')

for pkg_name in df["app_id"]:
    print(pkg_name, file=file_save)