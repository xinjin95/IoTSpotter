#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: download_images.py
@time: 4/8/21 10:06 PM
@desc:
"""
import json

metadata_path = "/home/xin/Documents/code/python/iot-measure/data/final_dataset/complete_dataset_metadata.txt"


def main():
    with open(metadata_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            screenshots = js["screenshots"]
