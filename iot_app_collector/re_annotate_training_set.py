#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: re_annotate_training_set.py
@time: 10/27/21 11:45 AM
@desc:
"""
import json

xin_iot_path1 = "../data/iot_annotation/xin_dataset_from_above_3.txt"
sunil_iot_path1 = "../data/iot_annotation/sunil_dataset_from_above_3.txt"

xin_iot_path2 = "../data/sp19_dataset/xin_dataset.txt"
sunil_iot_path2 = "../data/sp19_dataset/sunil_dataset.txt"

xin_non_iot_path = "../data/non_iot_annotation/xin_dataset.txt"
sunil_non_iot_path = "../data/non_iot_annotation/sunil_dataset.txt"

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

def get_xin_annotation():
    res = set()
    paths = [xin_non_iot_path, xin_iot_path1, xin_iot_path2]
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
    paths = [sunil_iot_path2, sunil_iot_path1, sunil_non_iot_path]
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

def get_all_annotated(xin_set, sunil_set):
    with open("../data/final_dataset/complete_dataset_metadata.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            line = line.strip('\n')
            app_id = js["app_id"]
            if app_id in xin_set:
                with open("../data/re_annotation_trainingset/xin_annotated.txt", 'a+') as xin:
                    print(line, file=xin)
            elif app_id in sunil_set:
                with open("../data/re_annotation_trainingset/sunil_annotated.txt", 'a+') as sunil:
                    print(line, file=sunil)
            else:
                print(line)

def main():
    all_apps = get_all_apps()
    xin_apps = get_xin_annotation()
    xin_apps = all_apps.intersection(xin_apps)
    print("# of apps:", len(xin_apps))
    sunil_apps = all_apps.difference(xin_apps)
    print("# of apps:", len(sunil_apps))
    # sunil_apps = get_snuil_apps()
    # original_apps = get_original_all()
    # sunil_improve_apps = all_apps.difference(original_apps)
    # sunil_apps = sunil_apps.union(sunil_improve_apps)
    # sunil_apps = all_apps.intersection(sunil_apps)
    # xin_apps = all_apps.difference(sunil_apps)
    # print("# of apps:", len(xin_apps))
    # print("# of apps:", len(sunil_apps))
    get_all_annotated(xin_apps, sunil_apps)


if __name__ == '__main__':
    main()