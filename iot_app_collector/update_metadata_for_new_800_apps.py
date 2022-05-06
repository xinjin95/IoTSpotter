#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: update_metadata_for_new_800_apps.py
@time: 5/13/21 11:22 AM
@desc:
"""
import json

import pandas as pd

save_path = "../data/final_dataset/complete_dataset_metadata.txt"
training_set_path = "../data/final_dataset/dataset_neural_networks/training_set.txt"
validation_set_path = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
test_set_path = "../data/final_dataset/dataset_neural_networks/test_set.txt"
metadata_path = "../data/final_dataset/add_800_training_set_metadata.txt"
csv_path = "../data/final_dataset/package_label_list.csv"
iot_app_set = set()


def get_apps(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            label = int(js["label"])
            if label == 1:
                iot_app_set.add(pkg_name)


def get_all_iot_apps():
    get_apps(training_set_path)
    get_apps(validation_set_path)
    get_apps(test_set_path)


def record_apps():
    pkg_names = []
    labels = []
    get_all_iot_apps()
    with open(save_path, 'w') as des:
        with open(metadata_path, 'r') as src:
            for line in src:
                js = json.loads(line)
                pkg_name = js["app_id"]
                if pkg_name in iot_app_set:
                    label = 1
                else:
                    label = 0
                pkg_names.append(pkg_name)
                labels.append(label)
                js["label"] = label
                print(json.dumps(js), file=des)
    df = pd.DataFrame({"pkg_name": pkg_names, "label": labels})
    df.to_csv(csv_path, index=False)


if __name__ == '__main__':
    record_apps()