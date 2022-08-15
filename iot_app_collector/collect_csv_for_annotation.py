#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: collect_csv_for_annotation.py
@time: 1/19/21 10:13 AM
@desc:
"""
import json

result_file = open("../data/package/annotation/corpus.csv", "a+")
existing_vendor = set([])

with open("../data/package/app_download/metadata_iot_apps.txt", 'r') as file:
    for i, line in enumerate(file):
        if i >= 200:
            continue
        js = json.loads(line)
        des = js["description"].replace(',', ';').replace('\n', '\t')
        developer = js["developer"]
        if developer in existing_vendor:
            continue
        existing_vendor.add(developer)
        print(des)
        package_name = js["app_id"]
        print("{},{},{}".format(package_name, des, developer), file=result_file)
