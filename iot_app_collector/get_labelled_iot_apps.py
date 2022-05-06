#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_labelled_iot_apps.py
@time: 2/9/21 10:03 AM
@desc:
"""
import json

path_save = "../data/iot-app/labelled_apps.txt"
file_save = open(path_save, 'a+')

with open("../data/keyword/IoT-seed.txt", 'r') as file:
    for line in file:
        js = json.loads(line)
        pkg_name = js["app_id"]
        des = js["description"]
        print(json.dumps({"pkg_name": pkg_name, "description": des}), file=file_save)