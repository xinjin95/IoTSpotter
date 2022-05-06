#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: analyze_static_results.py
@time: 6/14/21 11:50 PM
@desc:
"""
import json
import pandas as pd
import os
import numpy as np
from app_url_collector.dictionary import Dictionary

csv_path = "data/xin_sunil_shared_sha256_androzoo.csv"


def get_stats_per_app(result_path):
    with open(result_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            return js['chaStats']


def get_lib_per_app(result_path):
    with open(result_path, 'r') as file:
        for line in file:
            try:
                js = json.loads(line)
                return js['thirdPartyLibs'].keys()
            except:
                return set([])


def collect_lib_summary():
    lib_dict = dict()
    df = pd.read_csv(csv_path)
    apps_obfuscated = set()
    package_obfuscated = set()
    total = 0
    for i, pkg_name in enumerate(df["pkg_name"]):
        result_path = "data/lib_results/" + pkg_name + ".txt"
        print("{}-th: {}".format(i, pkg_name))
        if os.path.isfile(result_path): # total 36315
            res = get_lib_per_app(result_path)
            if len(res) == 0:
                continue
            total += 1
            # for package in res:
            #     if detect_obfuscation(package):
            #         print(package)
            #         apps_obfuscated.add(pkg_name)
            #         package_obfuscated.add(pkg_name + "," + package)
            #         continue
            #     if package not in lib_dict:
            #         lib_dict[package] = 0
            #     lib_dict[package] += 1
        else:
            print(pkg_name, "unavailable")
    # df = pd.DataFrame({"package_name": list(lib_dict.keys()), "frequency": list(lib_dict.values())})
    # df.to_csv("data/lib_frequency.csv", index=False)
    # lib_dict = Dictionary(lib_dict)
    # lib_dict = lib_dict.sort_by_value()
    # df = pd.DataFrame({"package_name": list(lib_dict.keys()), "frequency": list(lib_dict.values())})
    # df.to_csv("data/lib_frequency.csv", index=False)
    # write_to_file("data/obfuscation_details.txt", package_obfuscated)
    # write_to_file("data/obfuscation_pkg_names.txt", apps_obfuscated)
    print(total)


def get_average_frequency():
    csv_path = "data/lib_frequency.csv"
    df = pd.read_csv(csv_path)
    freq = df["frequency"]
    freq = np.asarray(freq) / 36315
    df["average_frequency"] = list(freq)
    df.to_csv("data/iot_lib_frequency.csv", index=False)


def write_to_file(file_name, src_set):
    with open(file_name, 'a+') as file:
        for src in src_set:
            print(src, file=file)


def detect_obfuscation(package_name):
    obfs = True
    pkgs = package_name.split('.')
    if len(pkgs[0]) == 1:
        return obfs
    for p in pkgs:
        if len(p) > 1:
            obfs = False
    return obfs


def compare_lib():
    df = pd.read_csv("data/non_iot_lib_frequency.csv")
    freq_dict = dict()
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, "dict")
        freq_dict[pkg_name] = [df["frequency"][i], df["average_frequency"][i]]
    df = pd.read_csv("data/iot_lib_frequency.csv")
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
    df.to_csv("data/compare_frequency.csv", index=False)


def get_diff():
    df = pd.read_csv("data/compare_frequency.csv")
    diff = []
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, 'compare')
        diff.append(df["non_iot_average_frequency"][i] - df["iot_average_frequency"][i])
    df["average_frequency_diff"] = diff
    df.to_csv("data/compare_frequency.csv", index=False)


def get_times():
    df = pd.read_csv("data/compare_frequency.csv")
    time_diff = []
    for i, pkg_name in enumerate(df["package_name"]):
        print(i, 'compare')
        if df["non_iot_average_frequency"][i] == 0:
            time_diff.append(100000000)
        else:
            time_diff.append(df["iot_average_frequency"][i] / df["non_iot_average_frequency"][i])
    df["average_frequency_division"] = time_diff
    df.to_csv("data/compare_frequency.csv", index=False)


def check_division():
    df = pd.read_csv("data/compare_frequency.csv")
    threshold = 500
    pkg_names = []
    des = open("data/iot_100_division/package_names_threshold_500.txt", 'a+')
    for i, div in enumerate(df["average_frequency_division"]):
        pkg_name = df["package_name"][i]
        if div > threshold:
            print(pkg_name, file=des)


if __name__ == '__main__':
    # app_result_path = "data/lib_results/a2dp.Vol.txt"
    # get_lib_per_app(app_result_path)
    # collect_lib_summary()
    # get_average_frequency()
    # compare_lib()
    # get_times()
    check_division()