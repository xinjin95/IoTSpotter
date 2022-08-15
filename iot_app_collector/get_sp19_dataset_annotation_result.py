#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_sp19_dataset_annotation_result.py
@time: 3/8/21 3:33 PM
@desc:
"""
import pandas as pd
import json

english_path = "../data/sp19_dataset/result/iot_annotation - english.csv"
english_save_path = "../data/sp19_dataset/result/annotation_english_result_checked.txt"

non_smart_home_path = "../data/sp19_dataset/result/iot_annotation - non_smart_home.csv"
non_smart_home_save_path = "../data/sp19_dataset/result/non_smart_home.txt"

annotation_from_above_3_path = "../data/iot_annotation/iot-app-annotation-from-above-3 - all.csv"
annotation_from_above_3_save_path = "../data/iot_annotation/annotation_from_above_3.txt"


def get_json_file_without_changing_label(file_path, file_save_path):
    df = pd.read_csv(file_path)
    with open(file_save_path, 'w+') as file:
        for i, pkg_name in enumerate(df["pkg_name"]):
            print(i)
            description = df['description'][i]
            label = int(df['label'][i])
            print(json.dumps({"pkg_name": pkg_name, "description": description, "label": label}), file=file)


def get_json_file(file_path, file_save_path):
    df = pd.read_csv(file_path)
    with open(file_save_path, 'w+') as file:
        for i, pkg_name in enumerate(df["pkg_name"]):
            description = df["description"][i]
            label = int(df['label'][i])
            if label == -1:
                label = 0
            print(json.dumps({"pkg_name": pkg_name, "description": description, "label": label}), file=file)


if __name__ == '__main__':
    # get_json_file(english_path, english_save_path)
    # get_json_file(non_smart_home_path, non_smart_home_save_path)
    get_json_file_without_changing_label(annotation_from_above_3_path, annotation_from_above_3_save_path)