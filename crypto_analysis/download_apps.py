#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: download_apps.py
@time: 12/14/21 2:42 PM
@desc:
"""
from utility.androzoo_download import download_apps
import pandas as pd

androzoo_download_csv = "data/app_download/androzoo_download.csv"
all_iot_csv = "../data/androzoo/description-improvement/xin_sunil_shared_sha256_androzoo.csv"


def get_target_csv():
    df = pd.read_csv(all_iot_csv)

