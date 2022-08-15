#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: iot_app_categories.py
@time: 8/10/21 3:36 PM
@desc:
"""
import pandas as pd
from classification.dictionary import Dictionary

csv_path = "data/iot_general_info.csv"

df = pd.read_csv(csv_path)

category_dict = dict()

for category in df["category"]:
    if category not in category_dict:
        category_dict[category] = 0
    category_dict[category] = category_dict[category] + 1

dictionary = Dictionary(category_dict)
category_dict = dictionary.sort_by_value()

df = pd.DataFrame({"category": list(category_dict.keys()), "num_apps": list(category_dict.values())})
df.to_csv("data/iot_category_distribution.csv", index=False)