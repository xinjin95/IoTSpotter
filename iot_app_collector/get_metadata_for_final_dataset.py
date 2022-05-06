#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_metadata_for_final_dataset.py
@time: 3/22/21 4:21 PM
@desc:
"""
import pandas as pd
import json

metadata_path = "../data/androzoo/app_metadata.json"
path_csv = "../data/final_dataset/package_label_list.csv"
path_save = "../data/final_dataset/complete_dataset_metadata.txt"


def get_metadata():
    df = pd.read_csv(path_csv)
    df_dict = {}
    for i, pkg_name in enumerate(df["app_id"]):
        df_dict[pkg_name] = int(df["label"][i])
    with open(path_save, 'w+') as des:
        with open(metadata_path, 'r') as file:
            for i, line in file:
                pkg_name, data = line.split(":", 1)
                print("{}-th: {}".format(i, pkg_name))
                if pkg_name in df_dict.keys():
                    js = json.loads(data)
                    js["label"] = df_dict[pkg_name]
                    print(json.dumps(js), file=des)
                    print("find it: " + pkg_name)


if __name__ == '__main__':
    get_metadata()