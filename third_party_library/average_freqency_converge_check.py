#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: average_freqency_converge_check.py
@time: 7/19/21 2:33 PM
@desc:
"""
import pandas as pd


package_num = 1000000
minimum_average_freq = 0.0001 # 20.0/200000

bench_mark_path = "data/non_iot_lib_frequency_200059.csv"
compared_path = "data/non_iot_lib_frequency_100300.csv"


def get_bench_mark_dict():
    df = pd.read_csv(bench_mark_path)
    lib_dict = dict()
    for i, pkg_name in enumerate(df["package_name"]):
        if i > package_num or df["average_frequency"][i] < minimum_average_freq:
            continue
        # print(i, pkg_name, df["frequency"][i], df["average_frequency"][i])
        lib_dict[pkg_name] = df["average_frequency"][i]
    return lib_dict


def compare():
    bench_mark_dict = get_bench_mark_dict()
    df = pd.read_csv(compared_path)
    pkg_names = []
    bench_mark_freq = []
    compared_freq = []
    diff_freq = []

    for i, pkg_name in enumerate(df["package_name"]):
        if pkg_name not in bench_mark_dict:
            continue
        pkg_names.append(pkg_name)
        bench_mark_freq.append(bench_mark_dict[pkg_name])
        compared_freq.append(df["average_frequency"][i])
        diff_freq.append(df["average_frequency"][i] - bench_mark_dict[pkg_name])
    df = pd.DataFrame({"package_name": pkg_names, "100K_average_freq": compared_freq, "200K_average_freq": bench_mark_freq,
                       "average_freq_diff": diff_freq})
    df.to_csv("data/average_freq_converage_check/200K_100K_average_compare.csv", index=False)


if __name__ == '__main__':
    # get_bench_mark_dict()
    compare()