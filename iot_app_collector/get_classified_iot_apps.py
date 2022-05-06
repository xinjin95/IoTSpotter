#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_classified_iot_apps.py
@time: 3/29/21 10:33 PM
@desc:
"""
import random

classification_result_path = "../data/androzoo/description-improvement/classification_result.csv"
all_iot_app_path = "../data/androzoo/description-improvement/classification_result_iot_apps.txt"
all_non_iot_app_path = "../data/androzoo/description-improvement/classification_result_non_iot_apps.txt"
sample_iot_path = "../data/androzoo/classification_result_inspection/iot_apps.txt"
sample_non_iot_path = "../data/androzoo/classification_result_inspection/non_iot_apps.txt"
iot_apps = []
non_iot_apps = []


def collect_iot_apps():
    with open(classification_result_path, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip('\n')
            pkg_name, res = line.split(',', 1)
            res = int(res)
            if res == 1:
                iot_apps.append(pkg_name)
            elif res == 0:
                non_iot_apps.append(pkg_name)
            else:
                print(line)
                exit(0)


def record_apps(file_path, pkg_list):
    with open(file_path, 'w+') as file:
        for pkg in pkg_list:
            print(pkg, file=file)


def sample_inspection_list(pkg_list, num_sample):
    return random.sample(pkg_list, num_sample)


def check_diff():
    iot_old = open("../data/androzoo/classification_result_iot_apps.txt", 'r').read().strip().split('\n')
    iot_new = open("../data/androzoo/description-improvement/classification_result_iot_apps.txt", 'r').read().strip().split('\n')
    iot_old = set(iot_old)
    iot_new = set(iot_new)

    print(len(iot_old))
    print(len(iot_new))
    print(len(iot_old.intersection(iot_new)))


if __name__ == '__main__':
    check_diff()
    # collect_iot_apps()
    # record_apps(all_iot_app_path, iot_apps)
    # record_apps(all_non_iot_app_path, non_iot_apps)
    # iot_samples = sample_inspection_list(iot_apps, 100)
    # non_iot_samples = sample_inspection_list(non_iot_apps, 100)
    # record_apps(sample_iot_path, iot_samples)
    # record_apps(sample_non_iot_path, non_iot_samples)