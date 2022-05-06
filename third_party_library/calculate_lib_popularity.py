#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: calculate_lib_popularity.py
@time: 8/22/21 11:19 PM
@desc:
"""
import os
import json

import pandas as pd
from classification.dictionary import Dictionary

iot_cluster_path = "data/iot_specific_lib_filter/prefix/package_names_prefix_3.txt"
pkg_name_app_mapping_path = "data/iot_specific_lib_app_name_mapping/iot_lib_map_ranked.txt"


def get_target_package_names():
    res = dict()
    with open(iot_cluster_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if line not in res:
                res[line] = set()
    return res


def get_prefix_2():
    res = dict()
    with open("data/iot_specific_lib_filter/prefix/package_names_prefix_2.txt", 'r') as f:
        for line in f:
            line = line.strip('\n')
            if line not in res:
                res[line] = set()
    return res


def get_cluster_app_mapping():
    mapping = get_target_package_names()

    print(" of clusters:", len(mapping))
    with open(pkg_name_app_mapping_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            pkg_name = js["package_name"]
            if pkg_name in mapping:
                mapping[pkg_name] = mapping[pkg_name].union(set(js["apps"]))
            else:
                tmp = pkg_name.split('.')
                assert len(tmp) > 3, "length error"
                pkg_name = '.'.join(tmp[:3])
                if pkg_name in mapping:
                    mapping[pkg_name] = mapping[pkg_name].union(set(js["apps"]))
                else:
                    print("unmapped", pkg_name)
    with open("general_statistics/iot_popularity/cluster_app_mapping.txt", 'w+') as des:
        for key, value in mapping.items():
            print(json.dumps({"cluster": key, "apps": list(value)}), file=des)
    pupularity = dict()
    for key, value in mapping.items():
        pupularity[key] = len(value)
    d = Dictionary(pupularity)
    pupularity = d.sort_by_value()
    df = pd.DataFrame({"cluster": list(pupularity.keys()), "app_num": list(pupularity.values())})
    df.to_csv("general_statistics/iot_popularity/cluster_popularity.csv", index=False)


def get_cluster_app_mapping_for_prefix_2():
    mapping = get_prefix_2()

    print(" of clusters:", len(mapping))
    with open(pkg_name_app_mapping_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            pkg_name = js["package_name"]
            if pkg_name in mapping:
                mapping[pkg_name] = mapping[pkg_name].union(set(js["apps"]))
            else:
                tmp = pkg_name.split('.')
                assert len(tmp) > 2, "length error"
                pkg_name = '.'.join(tmp[:2])
                if pkg_name in mapping:
                    mapping[pkg_name] = mapping[pkg_name].union(set(js["apps"]))
                else:
                    print("unmapped", pkg_name)
    with open("general_statistics/iot_popularity/cluster_app_mapping_prefix2.txt", 'w+') as des:
        for key, value in mapping.items():
            print(json.dumps({"cluster": key, "apps": list(value)}), file=des)
    pupularity = dict()
    for key, value in mapping.items():
        pupularity[key] = len(value)
    d = Dictionary(pupularity)
    pupularity = d.sort_by_value()
    df = pd.DataFrame({"cluster": list(pupularity.keys()), "app_num": list(pupularity.values())})
    df.to_csv("general_statistics/iot_popularity/cluster_popularity_prefix2.csv", index=False)

if __name__ == '__main__':
    # get_cluster_app_mapping()
    get_cluster_app_mapping_for_prefix_2()