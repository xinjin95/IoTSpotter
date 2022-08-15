#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: both_exist_converge.py
@time: 8/22/21 1:58 PM
@desc:
"""
import pandas as pd
import math

iot_pkg_path = "data/iot_lib_frequency.csv"
non_iot_pkg_path = "data/non_iot_converge/merged_average_freq.csv"
column_name = "_average_freq"


def calculate_diff(iot_freq, non_iot_freq):
    return abs(iot_freq - non_iot_freq) / non_iot_freq


def check_pkg_name_alignment():
    df_iot = pd.read_csv(iot_pkg_path)
    df_non_iot = pd.read_csv(non_iot_pkg_path)

    for i, pkg_name in enumerate(df_iot["package_name"]):
        pkg_name_non_iot = df_non_iot["package_name"][i]
        if pkg_name != pkg_name_non_iot:

            print(pkg_name, pkg_name_non_iot, i)
            return


def get_multiple_pkg_diff():
    iot_freq_dict = dict()
    df_iot = pd.read_csv(iot_pkg_path)
    df_non_iot = pd.read_csv(non_iot_pkg_path)
    for i, pkg_name in enumerate(df_iot["package_name"]):
        if i > 120000:
            break
        iot_freq_dict[pkg_name] = df_iot["iot_average_frequency"][i]

    non_iot_diff = dict()
    non_iot_diff["package_name"] = []
    for i, pkg_name in enumerate(df_non_iot["package_name"]):
        if i > 120000:
            break
        if pkg_name in iot_freq_dict:
            print(i)
            non_iot_diff["package_name"].append(pkg_name)
            for col in df_non_iot.columns:
                if col == "package_name":
                    continue
                non_iot_freq = df_non_iot[col][i]
                diff = calculate_diff(iot_freq_dict[pkg_name], non_iot_freq)
                if col not in non_iot_diff:
                    non_iot_diff[col] = []
                non_iot_diff[col].append(diff)

    df = pd.DataFrame(non_iot_diff)
    df.to_csv("data/non_iot_converge/merged_differential_analysis_both_exists.csv")


# def plot_random_packages():
#     with open()

if __name__ == '__main__':
    # check_pkg_name_alignment()
    get_multiple_pkg_diff()
