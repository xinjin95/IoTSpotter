#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_training_set_pkgs.py
@time: 5/11/21 12:16 AM
@desc:
"""
import json

training_set_path = "../data/final_dataset/dataset_neural_networks/training_set.txt"
validation_set_path = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
test_set_path = "../data/final_dataset/dataset_neural_networks/test_set.txt"
save_path = "../data/final_dataset/pkg_list.txt"
apps = set()


def collect_apps(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            apps.add(pkg_name)


def write_apps(file_path):
    with open(file_path, 'w+') as file:
        for app in apps:
            print(app, file=file)


if __name__ == '__main__':
    collect_apps(training_set_path)
    collect_apps(validation_set_path)
    collect_apps(test_set_path)
    write_apps(save_path)