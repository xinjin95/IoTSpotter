#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_combined_crypto_misuse_apps.py
@time: 1/31/22 9:11 PM
@desc:
"""
import pandas as pd

df = pd.read_csv("cognicrypt_results/accumulated_result_for_app.csv")
df = df[df['total_flaw_num'] > 0]
apps = set(df["app_name"])

df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
df = df[df['total_flaw_num'] > 0]
apps = apps.union(set(df["app_name"]))
print(len(apps))