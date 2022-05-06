#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_package_prefix.py
@time: 7/16/21 1:50 PM
@desc:
"""
import pandas as pd


def get_prefix():
    prefix_len = 3
    threshold = 500
    prefixs = set()
    prefix_list = list()
    with open("data/iot_100_division/package_names_threshold_{}.txt".format(threshold), 'r') as src:
        for line in src:
            line = line.strip('\n')
            lines = line.split('.')
            prefix = ""
            if len(lines) < prefix_len:
                prefix = line
            else:
                lines = lines[:prefix_len]
                prefix = '.'.join(lines)
                # print("")
            if prefix != "" and prefix not in prefixs:
                prefixs.add(prefix)
                prefix_list.append(prefix)
    with open("data/iot_100_division/package_names_prefix_{}_threshold_{}.txt".format(prefix_len, threshold), 'w+') as des:
        for prefix in prefix_list:
            print(prefix, file=des)


def get_initial_prefix():
    df = pd.read_csv("data/iot_lib_frequency.csv")
    for prefix_len in [2, 3, 4]:
        prefixs = set()
        prefix_list = list()
        for i, pkg_name in enumerate(df["package_name"]):
            lines = pkg_name.split('.')
            if len(lines) < prefix_len:
                prefix = pkg_name
            else:
                lines = lines[:prefix_len]
                prefix = '.'.join(lines)
            if prefix != "" and prefix not in prefixs:
                prefixs.add(prefix)
                prefix_list.append(prefix)
        with open("data/initial_iot_package_name_prefix/package_names_prefix_{}.txt".format(prefix_len),
                  'w+') as des:
            for prefix in prefix_list:
                print(prefix, file=des)


def get_iot_specific_prefix():
    for prefix_len in [2, 3, 4]:
        prefixs = set()
        prefix_list = list()
        df = pd.read_csv("data/iot_specific_lib_filter/only_in_non_iot_filtered.csv")
        for i, pkg_name in enumerate(df["package_name"]):
            lines = pkg_name.split('.')
            if len(lines) < prefix_len:
                prefix = pkg_name
            else:
                lines = lines[:prefix_len]
                prefix = '.'.join(lines)
            if prefix != "" and prefix not in prefixs:
                prefixs.add(prefix)
                prefix_list.append(prefix)
        df = pd.read_csv("data/iot_specific_lib_filter/both_exist_filtered.csv")
        for i, pkg_name in enumerate(df["package_name"]):
            lines = pkg_name.split('.')
            if len(lines) < prefix_len:
                prefix = pkg_name
            else:
                lines = lines[:prefix_len]
                prefix = '.'.join(lines)
            if prefix != "" and prefix not in prefixs:
                prefixs.add(prefix)
                prefix_list.append(prefix)
        with open("data/iot_specific_lib_filter/prefix/package_names_prefix_{}.txt".format(prefix_len),
                  'a+') as des:
            for prefix in prefix_list:
                print(prefix, file=des)


if __name__ == '__main__':
    # get_prefix()
    # get_initial_prefix()
    get_iot_specific_prefix()