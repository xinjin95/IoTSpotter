#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_developers.py
@time: 8/19/21 6:21 PM
@desc:
"""
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from calculate_rate import get_attribute, iot_app_metadata_path
from classification.dictionary import Dictionary

# iot_app_metadata_path = "../data/androzoo/description-improvement/new_shared_37K_metadata.txt"


def get_developer_names():
    save_path = "data/developer/iot_developer_name.csv"
    attr_name = "developer"
    get_attribute(iot_app_metadata_path, save_path, attr_name)


def get_developer_addr():
    save_path = "data/developer/iot_developer_addr.csv"
    attr_name = "developer_address"
    get_attribute(iot_app_metadata_path, save_path, attr_name)


def get_top_developers():
    save_path = "data/developer/iot_developer_name.csv"
    df = pd.read_csv(save_path)
    deve_dict = dict()
    for name in df["developer"]:
        if name not in deve_dict:
            deve_dict[name] = 0
        deve_dict[name] += 1
    dictionary = Dictionary(deve_dict)
    deve_dict = dictionary.sort_by_value()
    df = pd.DataFrame({"developer": list(deve_dict.keys()), "app_num": list(deve_dict.values())})
    df.to_csv("data/developer/iot_top_developer.csv", index=False)


def parse_developer_addr():
    save_path = "data/developer/iot_developer_addr.csv"
    df = pd.read_csv(save_path)
    for addr in df["developer_address"]:
        print(addr)

if __name__ == '__main__':
    # get_developer_names()
    # get_developer_addr()
    parse_developer_addr()