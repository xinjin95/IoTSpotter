#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_top_permission.py
@time: 8/20/21 3:55 PM
@desc:
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from classification.dictionary import Dictionary

manifest_path = "data/manifest_parse_result/merged_results.txt"


def get_permission():
    perm_dict = dict()
    total = 37212.0
    with open(manifest_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            # pkg_name = js["packageName"]
            if "uses-permission" in js:
                permissions = js["uses-permission"]
            else:
                permissions = []

            if "permission" in js:
                permissions += js["permission"]
            for permission in permissions:
                if permission not in perm_dict:
                    perm_dict[permission] = 0
                perm_dict[permission] += 1
    d = Dictionary(perm_dict)
    perm_dict = d.sort_by_value()
    percent = [v/total * 100 for v in list(perm_dict.values())]
    df = pd.DataFrame({"permission": list(perm_dict.keys()), "app_num": list(perm_dict.values()), "percent": percent})
    df.to_csv("data/permission/top_permission.csv", index=False)


if __name__ == '__main__':
    get_permission()