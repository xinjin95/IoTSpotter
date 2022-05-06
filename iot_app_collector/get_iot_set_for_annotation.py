#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_iot_set_for_annotation.py
@time: 3/12/21 6:14 PM
@desc:
"""
import json

path_above_three = "../data/iot_annotation/above_3.txt"
path_two = "../data/iot_annotation/twos.txt"
xin_dataset_path = "../data/iot_annotation/xin_dataset.txt"
sunil_dataset_path = "../data/iot_annotation/sunil_dataset.txt"


def build_annotation_set():
    with open(xin_dataset_path, 'w+') as xin_file:
        with open(sunil_dataset_path, 'w+') as sunil_file:
            with open(path_above_three, 'r') as file:
                for i, line in enumerate(file):
                    pkg_name, description = line.split(',', 1)
                    description = description.strip('\n').strip("\"")
                    js = {"pkg_name": pkg_name, "description": description}
                    if i < 859:
                        print(json.dumps(js), file=sunil_file)
                    else:
                        print(json.dumps(js), file=xin_file)

            sunil_range = range(0, )


def find_duplicates():
    dids = set()
    with open(path_above_three, 'r') as file:
        for i, line in enumerate(file):
            pkg_name, description = line.split(',', 1)
            if pkg_name in dids:
                print(pkg_name)
            dids.add(pkg_name)


if __name__ == '__main__':
    # build_annotation_set()
    find_duplicates()