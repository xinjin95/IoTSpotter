#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: count_dataset.py
@time: 10/5/21 7:53 PM
@desc:
"""
import json

app_list = "../data/final_dataset/pkg_list_800_added.txt"
test_path = "../data/final_dataset/dataset_neural_networks/test_set.txt"
training_path = "../data/final_dataset/dataset_neural_networks/training_set.txt"
validation_path = "../data/final_dataset/dataset_neural_networks/validation_set.txt"

iot_apps = set()
non_iot_apps = set()

def get_apps(file_path):
    apps = set()
    with open(file_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            app = js['pkg_name']
            if js["label"] == 1:
                iot_apps.add(app)
            else:
                non_iot_apps.add(app)
            apps.add(app)
    return apps

# iot: 2837, non iot: 3403
# iot: 414, non iot: 551

def main():
    all = open(app_list, 'r').read().strip('\n').split('\n')
    all = set(all)
    print("Total:", len(all))

    validation = get_apps(validation_path)
    training = get_apps(training_path)
    # print(f"iot: {len(iot_apps)}, non iot: {len(non_iot_apps)}")
    # iot_apps = set()
    # non_iot_apps = set()
    test = get_apps(test_path)
    print(len(test), len(training), len(validation))
    print("test set:", len(test))
    all = all.difference(test)
    training = all.intersection(training)
    all = all.difference(training)
    validation = all.intersection(validation)
    print("training set:", len(training))
    print("validation set:", len(validation))
    print(f"iot: {len(iot_apps)}, non iot: {len(non_iot_apps)}")

def check_numbers():
    test = get_apps(test_path)
    # validation = get_apps(validation_path)
    # training = get_apps(training_path)
    print(f"iot: {len(iot_apps)}, non iot: {len(non_iot_apps)}")

if __name__ == '__main__':
    # main()
    check_numbers()