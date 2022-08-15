#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: preprocess_test_apps.py
@time: 5/4/21 9:11 AM
@desc:
"""
import json
import os

metadata_600 = "../data/androzoo/600_inspection/600_metadata_with_label.txt"

iot_apps = set()
non_iot_apps = set()


def get_apps():
    with open(metadata_600, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            label = int(js["label"])
            if label == 1:
                iot_apps.add(pkg_name)
            elif label == 0:
                non_iot_apps.add(pkg_name)


def move_imgs():
    for fname in os.listdir("data/test_data/"):
        if not fname.endswith('.png'):
            continue
        # fpath = os.path.join("data/", fname)
        pkg_name = fname.replace('.png', '')
        if pkg_name in iot_apps:
            os.rename("data/test_data/{}".format(fname), "data/test_data/iot/{}".format(fname))
        elif pkg_name in non_iot_apps:
            os.rename("data/test_data/{}".format(fname), "data/test_data/non_iot/{}".format(fname))


if __name__ == '__main__':
    get_apps()
    move_imgs()