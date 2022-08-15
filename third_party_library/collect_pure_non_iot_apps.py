#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: collect_pure_non_iot_apps.py
@time: 7/12/21 10:07 AM
@desc:
"""
import pandas as pd

excluded_csv_path = "data/excluded_iot_shared_sha256.csv"
save_csv_path = "data/pure_non_iot_sha256.csv"
xxx_pre_iot_path = "../data/androzoo/classification_result_iot_apps.txt"
xxx_pre_iot_path = "../data/androzoo/xxx_iot_pkgs.txt"
xxx_new_iot_path = "../data/androzoo/description-improvement/classification_result_iot_apps.txt"
xxx_new_iot_path = "../data/androzoo/description-improvement/after_xxx_labeling_58K_pkgs.txt"
train_set_iot_path = "../data/final_dataset/pkg_list_800_added.txt"

iot_paths = [xxx_pre_iot_path, xxx_pre_iot_path, xxx_new_iot_path, xxx_new_iot_path, train_set_iot_path]


def collect_list(file_path):
    res = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip('\n')
            res.add(line)
    return res


def main():

    exclude_apps = set()
    for iot_path in iot_paths:
        exclude_apps |= collect_list(iot_path)
        print("# of apps:", len(exclude_apps))
    df = pd.read_csv(excluded_csv_path)
    res_pkg = []
    res_sha = []
    res_ver = []
    for i, pkg_name in enumerate(df["pkg_name"]):
        if pkg_name in exclude_apps:
            continue
        res_pkg.append(pkg_name)
        res_sha.append(df["sha256"][i])
        res_ver.append(df["vercode"][i])
    res = pd.DataFrame({"pkg_name": res_pkg, "sha256": res_sha, "vercode": res_ver})
    res.to_csv(save_csv_path, index=False)


if __name__ == '__main__':
    main()