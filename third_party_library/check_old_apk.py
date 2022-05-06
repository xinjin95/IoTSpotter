#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: check_old_apk.py
@time: 7/12/21 2:19 PM
@desc:
"""
import pandas as pd

old_2020_path = "../data/old_app_in_server/2020_06_pkgs.txt"
pure_csv_path = "data/pure_non_iot_sha256.csv"
save_pkgs_path = "data/old_pure_non_iot_pkgs.txt"


def get_available_pkgs(file_path):
    res = set()
    with open(file_path, 'r') as src:
        for line in src:
            line = line.strip('\n')
            res.add(line)
    return res


def main():
    old_apps = get_available_pkgs(old_2020_path)
    print("# of apps:", len(old_apps))
    df = pd.read_csv(pure_csv_path)
    with open(save_pkgs_path, 'w+') as des:
        for i, pkg_name in enumerate(df["pkg_name"]):
            if pkg_name not in old_apps:
                continue
            print(pkg_name, file=des)


if __name__ == '__main__':
    main()