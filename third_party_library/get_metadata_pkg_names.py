#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_metadata_pkg_names.txt.py
@time: 7/9/21 10:51 PM
@desc:
"""
import os

metadata_path = "../data/androzoo/app_metadata.json"
save_path = "../data/androzoo/all_2182654_pkg_names.txt"


def get_package_name():
    total = 0
    if os.path.isfile(save_path):
        os.remove(save_path)

    file_save = open(save_path, 'a+')
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, content = line.split(":", 1)
                    print(pkg_name, file=file_save)
                    total += 1
                    print(total)
                except:
                    print(line)


if __name__ == '__main__':
    get_package_name()