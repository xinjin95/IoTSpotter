#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: build_training_set.py
@time: 2/9/21 10:52 AM
@desc:
"""
import json
import os

path_training_set = "../data/dataset/training.txt"
path_test_set = "../data/dataset/test.txt"

original_iot_apps = "../data/iot-app/labelled_apps.txt"
more_iot_apps = "../data/iot-app/more_iot_apps.txt"

non_iot_apps = "../data/dataset/non_iot.txt"


def load_samples(path_file, path_save, label, num_sample=None):
    file_save = open(path_save, 'a+')
    used_apps = get_used_apps()
    total = 0
    with open(path_file, 'r') as file:
        for i, line in enumerate(file):
            if num_sample is not None and total > num_sample:
                continue
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            if pkg_name in used_apps:
                continue
            des = js["description"]
            print(json.dumps({"pkg_name": pkg_name, "description": des, "label": label}), file=file_save)
            total += 1


def check_duplication(path_file):
    used = set()
    if os.path.isfile(path_file):
        with open(path_file, 'r') as file:
            for line in file:
                try:
                    js = json.loads(line)
                    pkg_name = js["pkg_name"]
                    if pkg_name in used:
                        print(pkg_name)
                    used.add(pkg_name)
                except:
                    pass
    else:
        print("file no found")


def get_used_apps():
    res = set()
    if os.path.isfile(path_training_set):
        with open(path_training_set, 'r') as file:
            for line in file:
                try:
                    js = json.loads(line)
                    pkg_name = js["pkg_name"]
                    res.add(pkg_name)
                except:
                    pass
    if os.path.isfile(path_test_set):
        with open(path_test_set, 'r') as file:
            for line in file:
                try:
                    js = json.loads(line)
                    pkg_name = js["pkg_name"]
                    res.add(pkg_name)
                except:
                    pass
    return res


# load initial iot data to training
# load_samples(original_iot_apps, path_training_set, 1)

# load more iot apps to training
# load_samples(more_iot_apps, path_training_set, 1, 282)

# load test iot apps to testing
# load_samples(more_iot_apps, path_test_set, 1)

# load non iot apps to training
# load_samples(non_iot_apps, path_training_set, 0, 291)

# load non iot apps to testing
# load_samples(non_iot_apps, path_test_set, 0, 143)

# check duplication
# check_duplication(path_training_set)
check_duplication(path_test_set)