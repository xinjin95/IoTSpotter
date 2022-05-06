#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_top_use_feature.py
@time: 8/20/21 5:54 PM
@desc:
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from classification.dictionary import Dictionary

manifest_path = "data/manifest_parse_result/merged_results.txt"


def calculate_activity():
    pkg_names = []
    feature_nums = []
    with open(manifest_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["packageName"]
            if "uses-feature-true" in js:
                feature = js["uses-feature-true"]
            else:
                feature = []
            feature_num = len(feature)
            pkg_names.append(pkg_name)
            feature_nums.append(feature_num)
    df = pd.DataFrame({"package_name": pkg_names, "feature_num": feature_nums})
    df.to_csv("data/feature/feature_num.csv", index=False)


def get_top_features():
    feature_dict = dict()
    total = 37213.0
    with open(manifest_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["packageName"]
            if "uses-feature-true" in js:
                feature = js["uses-feature-true"]
            else:
                feature = []
            for f in feature:
                if f not in feature_dict:
                    feature_dict[f] = 0
                feature_dict[f] += 1
    d = Dictionary(feature_dict)
    feature_dict = d.sort_by_value()
    percent = [p/total * 100 for p in list(feature_dict.values())]
    df = pd.DataFrame({"feature": list(feature_dict.keys()), "app_num": list(feature_dict.values()), "percent": percent})
    df.to_csv("data/feature/top_feature.csv", index=False)


if __name__ == '__main__':
    # calculate_activity()
    get_top_features()