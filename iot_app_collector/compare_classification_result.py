#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: compare_classification_result.py
@time: 3/30/21 11:23 AM
@desc:
"""
import random

xxx_path = "../data/androzoo/iot_predicted_xxx_63k.txt"
# xxx_list_path = "../data/androzoo/xxx_iot_pkgs.txt"
# xxx_list_path = "../data/androzoo/classification_result_iot_apps.txt"
xxx_list_path = "../data/androzoo/description-improvement/after_xxx_labeling_58K_pkgs.txt"
xxx_list_path = "../data/androzoo/description-improvement/classification_result_iot_apps.txt"


def get_xxx_apps():
    file_save = open(xxx_list_path, 'a+')
    with open(xxx_path, 'r') as file:
        for line in file:
            pkg_name, des = line.split('\t', 1)
            print(pkg_name, file=file_save)


def load_apps(file_path):
    apps = []
    with open(file_path, 'r') as file:
        for line in file:
            apps.append(line.strip('\n'))
    return apps


def compare():
    xxx_apps = load_apps(xxx_list_path)
    xxx_apps = set(xxx_apps)
    print(len(xxx_apps))
    xxx_apps = load_apps(xxx_list_path)
    xxx_apps = set(xxx_apps)
    print(len(xxx_apps))
    print(len(xxx_apps.intersection(xxx_apps)))
    shared = xxx_apps.intersection(xxx_apps)

    # with open("../data/androzoo/description-improvement/xxx_xxx_non_shared_pkgs.txt", 'w+') as file:
    #     for app in :
    #         print(app, file=file)

    non_shared = xxx_apps.union(xxx_apps)
    non_shared = non_shared.difference(shared)
    with open("../data/androzoo/description-improvement/xxx_xxx_non_shared_pkgs.txt", 'w+') as file:
        for app in non_shared:
            print(app, file=file)
    # with open("../data/androzoo/description-improvement/xxx_xxx_classification_result_union.txt", 'w+') as file:
    #     for app in non_shared.union(shared):
    #         print(app, file=file)
    print(len(non_shared))
    xxx_unshared = xxx_apps.intersection(non_shared)
    xxx_unshared = xxx_apps.intersection(non_shared)
    # samples = random.sample(xxx_unshared, 250)
    with open("../data/androzoo/description-improvement/xxx_unique.txt", 'w+') as des:
        for app in xxx_unshared:
            print(app, file=des)
    # samples = random.sample(xxx_unshared, 250)
    with open("../data/androzoo/description-improvement/xxx_unique.txt", 'w+') as des:
        for app in xxx_unshared:
            print(app, file=des)
    print(len(xxx_unshared), len(xxx_unshared))


if __name__ == '__main__':
    compare()