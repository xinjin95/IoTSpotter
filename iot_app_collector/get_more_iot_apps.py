#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_more_iot_apps.py
@time: 2/9/21 9:33 AM
@desc:
"""
import json
import langid
from iot_app_collector.text_processor import TextProcessor

checked_apps = open("../data/iot-app/already_checked_list.txt",'r').read().strip().split('\n')
checked_apps = set(checked_apps)
seed_iot_apps = set()
more_iot_apps = "../data/iot-app/already_checked_list.txt"
file_more_iot_apps = open(more_iot_apps, 'a+')

with open("../data/package/app_download/metadata_iot_apps.txt", 'r') as file:
    tp = TextProcessor("")
    for line in file:
        js = json.loads(line)
        pkg_name = js['app_id']
        if pkg_name not in checked_apps:
            seed_iot_apps.add(pkg_name)
            des = js['description']
            language = langid.classify(des)[0]
            if language != 'en':
                print("{}, {}".format(pkg_name, language))
                print(des)
            else:
                tp.text = des
                description_processed = tp.process()
                print(json.dumps({"pkg_name": pkg_name, "description": description_processed}), file=file_more_iot_apps)