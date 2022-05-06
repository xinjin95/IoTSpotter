#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_metadata_info.py
@time: 8/10/21 3:40 PM
@desc:
"""
import json
import os
import pandas as pd

app_list_path = "../data/androzoo/description-improvement/xin_sunil_shared_pkgs.txt"
metadata_path = "../data/androzoo/description-improvement/new_shared_37K_metadata.txt"

save_path = "data/iot_general_info.csv"


def main():
    pkg_names = []
    categories = []
    installs = []
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(metadata_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            pkg_names.append(js['app_id'])
            if js["category"][0].lower().startswith("game"):
                categories.append("GAME")
            else:
                categories.append(js["category"][0])
            installs.append(js["installs"].replace(',', '').replace('+', ''))
    df = pd.DataFrame({"package_name": pkg_names,
                       "category": categories,
                       "install_num": installs})
    df.to_csv(save_path)


if __name__ == '__main__':
    main()