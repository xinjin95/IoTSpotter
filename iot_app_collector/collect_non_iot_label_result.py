#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: collect_non_iot_label_result.py
@time: 3/22/21 10:44 AM
@desc:
"""
import pandas as pd
import json
file_path = "../data/non_iot_annotation/result/xxx_dataset_labeled.csv"
file_save_path = "../data/non_iot_annotation/result/xxx_dataset_need_confirm.txt"


def get_json_file():
    df = pd.read_csv(file_path)
    with open(file_save_path, 'w+') as file:
        for i, pkg_name in enumerate(df["pkg_name"]):
            description = df["description"][i]
            label = int(df['label'][i])
            if label == -1:
                continue
            if label == 1:
                print(json.dumps({"pkg_name": pkg_name, "description": description, "label": label}), file=file)


if __name__ == '__main__':
    get_json_file()