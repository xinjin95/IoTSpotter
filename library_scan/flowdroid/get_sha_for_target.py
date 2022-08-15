#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_sha_for_target.py
@time: 8/4/21 10:51 AM
@desc:
"""
import pandas as pd
from large_scale_scan import get_app_list

src_sha_path = "../../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv"
des_sha_path = "data/target_sha.csv"

app_names = get_app_list()

df = pd.read_csv(src_sha_path)

new_df = df[df["pkg_name"].isin(app_names)]

new_df.to_csv(des_sha_path, index=False)