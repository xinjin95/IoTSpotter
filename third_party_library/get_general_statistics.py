#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_general_statistics.py
@time: 8/21/21 10:23 PM
@desc:
"""
import os
import json
import glob

import pandas as pd

root_dir = "data/lib_results/"
target_app_path = "../data/androzoo/description-improvement/xin_sunil_shared_pkgs.txt"
general_statistics = "general_statistics/lib_cha_statistics.txt"


def get_app_set() -> set:
    res = set()
    with open(target_app_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            res.add(line)
    return res


def collect_cha_statistics():
    apps = get_app_set()
    print("# of apps:", len(apps))
    files = glob.glob(root_dir + '*')
    with open(general_statistics, 'a+') as des:
        for i, file in enumerate(files):
            print(i, file)
            app_name = os.path.basename(file)
            if not app_name.endswith(".txt"):
                continue
            app_name = app_name.replace('.txt', '')
            if app_name not in apps:
                print("[-] not in:", app_name)
                continue
            with open(file, 'r') as src:
                for line in src:
                    try:
                        js = json.loads(line)
                        chaStats = js["chaStats"]
                        chaStats["package_name"] = app_name
                        des.write(json.dumps(chaStats) + '\n')
                    except:
                        print("")


def calculate_general_statistics():
    res = dict()
    with open(general_statistics, 'r') as f:
        for line in f:
            js = json.loads(line)
            for key, value in js.items():
                if key not in res and key != "package_name":
                    res[key] = 0
                if key != "package_name":
                    res[key] += value
    df = pd.DataFrame({"name": list(res.keys()), "value": list(res.values())})
    df.to_csv("general_statistics/accumulative_cha.csv")


if __name__ == '__main__':
    # collect_cha_statistics()
    calculate_general_statistics()