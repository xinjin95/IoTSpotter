#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: plot_iot_specific_freq.py
@time: 7/27/21 10:17 AM
@desc:
"""
import pandas as pd
import matplotlib.pyplot as plt
from dictionary import Dictionary


only_iot_path = "data/iot_specific_lib_filter/only_in_iot.csv"
both_exist_path = "data/iot_specific_lib_filter/both_exist.csv"


def plot_only_iot():
    iot_freq_dict = dict()
    df = pd.read_csv(only_iot_path)
    for iot_freq in df["iot_frequency"]:
        iot_freq = int(iot_freq)
        if iot_freq not in iot_freq_dict:
            iot_freq_dict[iot_freq] = 0
        iot_freq_dict[iot_freq] += 1
    dictionary = Dictionary(iot_freq_dict)
    iot_freq_dict = dictionary.sort_by_key()
    x = list(iot_freq_dict.keys())
    y = list(iot_freq_dict.values())
    df = pd.DataFrame({"iot_freq": x, "num_package_names": y})
    df.to_csv("data/iot_specific_lib_filter/only_iot_iot_frequency_distribution.csv", index=False)
    plt.bar(x, y, align='center', alpha=0.5)
    plt.xlabel("iot_frequency")
    plt.ylabel("# of package names")
    plt.title("How many package names have that iot_frequency")
    plt.show()


def plot_both_exist():
    iot_freq_dict = dict()
    df = pd.read_csv(both_exist_path)
    for division_time in df["average_frequency_division"]:
        division_time = int(division_time)
        division_time = division_time//10 * 10
        if division_time not in iot_freq_dict:
            iot_freq_dict[division_time] = 0
        iot_freq_dict[division_time] += 1
    dictionary = Dictionary(iot_freq_dict)
    iot_freq_dict = dictionary.sort_by_key()
    x = list(iot_freq_dict.keys())
    y = list(iot_freq_dict.values())
    df = pd.DataFrame({"iot_dividing_non_iot_average_freq": x, "num_package_names": y})
    df.to_csv("data/iot_specific_lib_filter/both_exist_division_distribution.csv", index=False)
    plt.bar(x, y, align='center', alpha=0.5)
    plt.xlabel("iot_dividing_non_iot_average_freq")
    plt.ylabel("# of package names")
    plt.title("How many package names have that average_frequency_division")
    plt.show()


if __name__ == '__main__':
    # plot_only_iot()
    plot_both_exist()