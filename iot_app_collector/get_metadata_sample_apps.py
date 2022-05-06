#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_metadata_sample_apps.py
@time: 3/29/21 10:50 PM
@desc:
"""

import argparse
import json


def get_apps(file_path):
    apps = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            apps.append(line)
    return apps


def get_metadata(metadata_path, app_list, save_path):
    app_list = set(app_list)
    total = 0
    file_save = open(save_path, 'a+')
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, content = line.split(":", 1)
                    if pkg_name in app_list:
                        print(json.dumps(json.loads(content)), file=file_save)
                    total += 1
                    print(total)
                except:
                    print(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--metadata_path", type=str, required=True)
    parser.add_argument("-a", "--app_list_path", type=str, required=True)
    parser.add_argument("-s", "--save_path", type=str, required=True)

    args = parser.parse_args()

    metadata_path = args.metadata_path
    app_list_path = args.app_list_path
    save_path = args.save_path

    target_apps = get_apps(app_list_path)
    get_metadata(metadata_path, target_apps, save_path)