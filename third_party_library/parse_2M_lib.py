#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: parse_2M_lib.py
@time: 7/13/21 10:14 AM
@desc:
"""

import json
import time

import pandas as pd
import os
import numpy as np
import glob
from dictionary import Dictionary
from copy import deepcopy

lib_results_path = "data/2M_lib_results/"
# save_path = "data/200K_package_names_new.txt"
finished_path = ["data/2M_lib_log/97K_package_names.txt", "data/2M_lib_log/200K_package_names_new.txt"]
save_path = "data/2M_lib_log/380K_package_names_new.txt"
finished = set()


def get_lib_per_app(result_path):
    with open(result_path, 'r') as file:
        for line in file:
            try:
                js = json.loads(line)
                return js['thirdPartyLibs'].keys()
            except:
                return set([])


def get_finished():
    for path_path in finished_path:
        with open(path_path, 'r') as src:
            for line in src:
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                finished.add(pkg_name)


def collect_package_names():
    files = glob.glob(lib_results_path + '*')
    get_finished()
    print("# of finished:", len(finished))
    print("# of files:", len(files))
    # if collect_new:
    #     save_path = "data/200K_package_names_new.txt"
    with open(save_path, 'w+') as des:
        for i, file in enumerate(files):
            #
            if not file.endswith('.txt'):
                continue
            print(i, "-th file:", file)
            base_file = os.path.basename(file)
            base_file = base_file[:-4]
            if base_file in finished:
                print("[-] finished on:", base_file)
                continue
            res = {"pkg_name": base_file, "libs": list(get_lib_per_app(file))}
            print(json.dumps(res), file=des)
            # with open(file, 'r') as src:
            #     for line in src:
            #         js = json.loads(line)


def get_lib_distribution(file_path, lib_dict):
    total = 0
    with open(file_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            print(i, "-th line", pkg_name)
            libs = js["libs"]
            if len(libs) == 0:
                continue
            total += 1
            for package in libs:
                if package not in lib_dict:
                    lib_dict[package] = 0
                lib_dict[package] += 1

    return total, lib_dict


def get_non_iot_lib_frequency():
    lib_dict = dict()
    total, lib_dict = get_lib_distribution("data/97K_package_names.txt", lib_dict)
    total1, lib_dict = get_lib_distribution("data/200K_package_names_new.txt", lib_dict)
    total += total1
    print("total # of pkg_names", total)
    lib_dict = Dictionary(lib_dict)
    lib_dict = lib_dict.sort_by_value()
    lib_names = list(lib_dict.keys())
    lib_freq = list(lib_dict.values())
    lib_freq_ave = np.asarray(lib_freq)
    lib_freq_ave = lib_freq_ave / total
    df = pd.DataFrame({"package_name": lib_names, "frequency": lib_freq, "average_frequency": list(lib_freq_ave)})
    df.to_csv("data/non_iot_lib_frequency_{}.csv".format(total), index=False)


src_files = ["data/97K_package_names.txt", "data/200K_package_names_new.txt", "data/380K_package_names_new.txt"]


def calculate_average_freq(num_apps, lib_dict):
    total = 0
    # lib_dict = dict()
    print("[*] num_apps:", num_apps)
    print("[*] android.support.v4.app", lib_dict["android.support.v4.app"])
    time.sleep(5)
    for src_file in src_files:
        with open(src_file, 'r') as src:
            for i, line in enumerate(src):
                if total > num_apps:
                    break
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                print("\t", i, "-th line", pkg_name)
                libs = js["libs"]
                if len(libs) == 0:
                    continue
                total += 1
                for package in libs:
                    if package in lib_dict:
                        lib_dict[package] += 1
    for key, value in lib_dict.items():
        lib_dict[key] = value * 1.0 / total
    return total, lib_dict


def get_base_dict():
    lib_dict = dict()
    df = pd.read_csv("data/average_freq_converage_check/200K_100K_average_compare.csv")
    for pkg_name in df["package_name"]:
        lib_dict[pkg_name] = 0
    return lib_dict


def calculate_overall_distribution():
    # total = 388367
    step_num = 38837
    base_freq_dict = get_base_dict()
    df = pd.read_csv("data/average_freq_converage_check/200K_100K_average_compare.csv")
    for i in range(1, 11):

        total_app, lib_dict = calculate_average_freq(step_num * i, deepcopy(base_freq_dict))

        save_path = "data/non_iot_converge/{}_average_freq.csv".format(step_num * i)
        save_file = open(save_path, 'a+')
        print("package_name,average_freq", file=save_file)
        print("Save to file:", save_path)
        for pkg_name in df["package_name"]:
            print("{},{}".format(pkg_name, lib_dict[pkg_name]), file=save_file)


def merge_csv():
    step_num = 38837
    df = pd.read_csv("data/average_freq_converage_check/200K_100K_average_compare.csv")
    res = dict()
    res["package_name"] = list(df["package_name"])
    for i in range(1, 11):
        key = "{}_average_freq".format(step_num * i)
        save_path = "data/non_iot_converge/{}_average_freq.csv".format(step_num * i)
        df = pd.read_csv(save_path)
        res[key] = list(df["average_freq"])
    df = pd.DataFrame(res)
    df.to_csv("data/non_iot_converge/merged_average_freq.csv", index=False)


if __name__ == '__main__':
    # collect_package_names()
    # get_non_iot_lib_frequency()
    # calculate_overall_distribution()
    merge_csv()