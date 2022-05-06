#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: check_dataset_duplication.py
@time: 2/28/21 8:38 PM
@desc:
"""

import json

path_training = "../data/dataset/training_large.txt"
path_test = "../data/dataset/testing_large.txt"

dids = set()

def read_apps(path_file):
    with open(path_file, 'r') as file:
        for line in file:
            js = json.loads(line)
            app_id = js["pkg_name"]
            if app_id in dids:
                print(app_id)
            dids.add(app_id)

read_apps(path_training)
read_apps(path_test)