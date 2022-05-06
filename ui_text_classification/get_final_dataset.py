#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_final_dataset.py
@time: 4/26/21 6:48 PM
@desc:
"""
import json

iot_app_path = "../data/ui_text_dataset/annotation/result/iot_app_list.txt"
non_iot_app_path = "../data/ui_text_dataset/annotation/result/non_iot_app_list.txt"
training_ui_path = "../data/ui_text_dataset/neural_net/training_set.txt"
app_set = set()


def get_apps(file_path) -> set:
    apps = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip('\n')
            apps.add(line)
    return apps


def sample_dataset():
    lines = []
    with open(training_ui_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            label = js["label"]
            pkg_name = js["pkg_name"]
            if pkg_name in app_set:
                lines.append(js)
    with open("../data/ui_text_dataset/annotation/result/ui_text_dataset.txt", 'w+') as file:
        for js in lines:
            print(json.dumps(js), file=file)


def get_app_set():
    iot_apps = get_apps(iot_app_path)
    non_iot_apps = get_apps(non_iot_app_path)
    app_set = iot_apps.union(non_iot_apps)
    return app_set


if __name__ == '__main__':
    sample_dataset()