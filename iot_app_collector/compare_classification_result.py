#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: compare_classification_result.py
@time: 3/30/21 11:23 AM
@desc:
"""
import random

sunil_path = "../data/androzoo/iot_predicted_sunil_63k.txt"
# sunil_list_path = "../data/androzoo/sunil_iot_pkgs.txt"
# xin_list_path = "../data/androzoo/classification_result_iot_apps.txt"
sunil_list_path = "../data/androzoo/description-improvement/after_sunil_labeling_58K_pkgs.txt"
xin_list_path = "../data/androzoo/description-improvement/classification_result_iot_apps.txt"


def get_sunil_apps():
    file_save = open(sunil_list_path, 'a+')
    with open(sunil_path, 'r') as file:
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
    sunil_apps = load_apps(sunil_list_path)
    sunil_apps = set(sunil_apps)
    print(len(sunil_apps))
    xin_apps = load_apps(xin_list_path)
    xin_apps = set(xin_apps)
    print(len(xin_apps))
    print(len(xin_apps.intersection(sunil_apps)))
    shared = xin_apps.intersection(sunil_apps)

    # with open("../data/androzoo/description-improvement/xin_sunil_non_shared_pkgs.txt", 'w+') as file:
    #     for app in :
    #         print(app, file=file)

    non_shared = xin_apps.union(sunil_apps)
    non_shared = non_shared.difference(shared)
    with open("../data/androzoo/description-improvement/xin_sunil_non_shared_pkgs.txt", 'w+') as file:
        for app in non_shared:
            print(app, file=file)
    # with open("../data/androzoo/description-improvement/xin_sunil_classification_result_union.txt", 'w+') as file:
    #     for app in non_shared.union(shared):
    #         print(app, file=file)
    print(len(non_shared))
    sunil_unshared = sunil_apps.intersection(non_shared)
    xin_unshared = xin_apps.intersection(non_shared)
    # samples = random.sample(sunil_unshared, 250)
    with open("../data/androzoo/description-improvement/sunil_unique.txt", 'w+') as des:
        for app in sunil_unshared:
            print(app, file=des)
    # samples = random.sample(xin_unshared, 250)
    with open("../data/androzoo/description-improvement/xin_unique.txt", 'w+') as des:
        for app in xin_unshared:
            print(app, file=des)
    print(len(sunil_unshared), len(xin_unshared))


if __name__ == '__main__':
    compare()