#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: iot_specific_lib_filter.py
@time: 7/19/21 3:35 PM
@desc:
"""
import pandas as pd

minimum_average_freq = 0.0001
iot_package_freq = "data/iot_lib_frequency.csv"
non_iot_package_freq = "data/non_iot_lib_frequency_200059.csv"
save_csv_path = "data/iot_specific_lib_filter/compare_frequency_200059.csv"


def get_non_iot_average_freq_dict():
    df = pd.read_csv(non_iot_package_freq)
    lib_dict = dict()
    for i, pkg_name in enumerate(df["package_name"]):
        # if df["average_frequency"][i] < minimum_average_freq:
        #     continue
        # print(i, pkg_name, df["frequency"][i], df["average_frequency"][i])
        lib_dict[pkg_name] = [df["frequency"][i], df["average_frequency"][i]]
    return lib_dict


def compare_lib():
    freq_dict = get_non_iot_average_freq_dict()
    df = pd.read_csv(iot_package_freq)
    non_iot_freq = []
    non_iot_freq_ave = []
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, 'compare')
        if pkg_name in freq_dict:
            non_iot_freq.append(freq_dict[pkg_name][0])
            non_iot_freq_ave.append(freq_dict[pkg_name][1])
        else:
            non_iot_freq.append(0)
            non_iot_freq_ave.append(0)
    df["non_iot_frequency"] = non_iot_freq
    df["non_iot_average_frequency"] = non_iot_freq_ave
    df.to_csv(save_csv_path, index=False)
    print("Compared the non-iot frequency")


def get_diff():
    df = pd.read_csv(save_csv_path)
    diff = []
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, 'calculate diff')
        diff.append(df["non_iot_average_frequency"][i] - df["iot_average_frequency"][i])
    df["average_frequency_diff"] = diff
    df.to_csv(save_csv_path, index=False)


def get_times():
    df = pd.read_csv(save_csv_path)
    time_diff = []
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, 'calculate times')
        if df["non_iot_average_frequency"][i] == 0:
            time_diff.append(100000000)
        else:
            time_diff.append(df["iot_average_frequency"][i] / df["non_iot_average_frequency"][i])
    df["average_frequency_division"] = time_diff
    df.to_csv(save_csv_path, index=False)


def main():
    compare_lib()
    get_diff()
    get_times()


def split_for_inspection():
    df = pd.read_csv(save_csv_path)
    non_iot_non_exist_list = []
    for i, freq_div in enumerate(df["average_frequency_division"]):
        if freq_div != 100000000:
            non_iot_non_exist_list.append(i)
    print("# of lib to drop:", len(non_iot_non_exist_list))
    new_df = df.drop(non_iot_non_exist_list)
    new_df.to_csv("data/iot_specific_lib_filter/only_in_non_iot.csv")


minimum_times_both = 40 # and the
minimum_iot_freq = 7 # I cannot find more info for the rest ones.


def filter_target_package_names():
    df = pd.read_csv("data/iot_specific_lib_filter/only_in_non_iot.csv")
    excluded_list = []
    for i, freq in enumerate(df["iot_frequency"]):
        if freq < minimum_iot_freq:
            excluded_list.append(i)
    new_df = df.drop(excluded_list)
    new_df.to_csv("data/iot_specific_lib_filter/only_in_non_iot_filtered.csv")

    df = pd.read_csv("data/iot_specific_lib_filter/both_exist.csv")
    excluded_list = []
    for i, freq_div in enumerate(df["average_frequency_division"]):
        if freq_div < minimum_times_both:
            excluded_list.append(i)
    new_df = df.drop(excluded_list)
    new_df.to_csv("data/iot_specific_lib_filter/both_exist_filtered.csv")


if __name__ == '__main__':
    # main()
    # split_for_inspection()
    filter_target_package_names()