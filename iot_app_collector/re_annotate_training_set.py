#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: re_annotate_training_set.py
@time: 10/27/21 11:45 AM
@desc:
"""
import json

xxx_iot_path1 = "../data/iot_annotation/xxx_dataset_from_above_3.txt"
xxx_iot_path1 = "../data/iot_annotation/xxx_dataset_from_above_3.txt"

xxx_iot_path2 = "../data/sp19_dataset/xxx_dataset.txt"
xxx_iot_path2 = "../data/sp19_dataset/xxx_dataset.txt"

xxx_non_iot_path = "../data/non_iot_annotation/xxx_dataset.txt"
xxx_non_iot_path = "../data/non_iot_annotation/xxx_dataset.txt"

final_pkg_path = "../data/final_dataset/pkg_list_800_added.txt"
original_pkg_path = "../data/final_dataset/training_set_list.txt"

def get_all_apps():
    res = set()
    with open(final_pkg_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            res.add(line)
    print("# of apps:", len(res))
    return res


def get_original_all():
    res = set()
    with open(original_pkg_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            res.add(line)
    print("# of apps:", len(res))
    return res

def get_xxx_annotation():
    res = set()
    paths = [xxx_non_iot_path, xxx_iot_path1, xxx_iot_path2]
    for path in paths:
        with open(path, 'r') as f:
            for line in f:
                js = json.loads(line)
                if "pkg_name" in js:
                    res.add(js["pkg_name"])
                elif "app_id" in js:
                    res.add(js["app_id"])
                else:
                    print(path)
    print("# of apps:", len(res))
    return res


def get_snuil_apps():
    res = set()
    paths = [xxx_iot_path2, xxx_iot_path1, xxx_non_iot_path]
    for path in paths:
        with open(path, 'r') as f:
            for line in f:
                js = json.loads(line)
                if "pkg_name" in js:
                    res.add(js["pkg_name"])
                elif "app_id" in js:
                    res.add(js["app_id"])
                else:
                    print(path)
    print("# of apps:", len(res))
    return res

def get_all_annotated(xxx_set, xxx_set):
    with open("../data/final_dataset/complete_dataset_metadata.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            line = line.strip('\n')
            app_id = js["app_id"]
            if app_id in xxx_set:
                with open("../data/re_annotation_trainingset/xxx_annotated.txt", 'a+') as xxx:
                    print(line, file=xxx)
            elif app_id in xxx_set:
                with open("../data/re_annotation_trainingset/xxx_annotated.txt", 'a+') as xxx:
                    print(line, file=xxx)
            else:
                print(line)

def main():
    all_apps = get_all_apps()
    xxx_apps = get_xxx_annotation()
    xxx_apps = all_apps.intersection(xxx_apps)
    print("# of apps:", len(xxx_apps))
    xxx_apps = all_apps.difference(xxx_apps)
    print("# of apps:", len(xxx_apps))
    # xxx_apps = get_snuil_apps()
    # original_apps = get_original_all()
    # xxx_improve_apps = all_apps.difference(original_apps)
    # xxx_apps = xxx_apps.union(xxx_improve_apps)
    # xxx_apps = all_apps.intersection(xxx_apps)
    # xxx_apps = all_apps.difference(xxx_apps)
    # print("# of apps:", len(xxx_apps))
    # print("# of apps:", len(xxx_apps))
    get_all_annotated(xxx_apps, xxx_apps)


if __name__ == '__main__':
    main()