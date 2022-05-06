#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: calculate_apk_size.py
@time: 8/19/21 3:45 PM
@desc:
"""
import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


save_path = "data/apk_size/all_size.csv"


def get_file_size(metadata_path, app_list, save_path):
    if app_list is not None:
        app_list = set(app_list)
    total = 0
    file_save = open(save_path, 'a+')
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines(10000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, content = line.split(":", 1)
                    if app_list is None or pkg_name in app_list:
                        js = json.loads(content)
                        print(pkg_name + ',' + js["size"], file=file_save)
                    total += 1
                    print(total)
                except:
                    print(line)


def check_size_unit():
    units = set()
    with open(save_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            unit = line[-1]
            # print(line[-1])
            if unit not in units:
                units.add(unit)
                print(unit, line)
    print(units)


def get_all_sizes():
    metadata_path = "../data/androzoo/app_metadata.json"
    app_list = None

    get_file_size(metadata_path, app_list, save_path)


def get_big_range_iot_pkgs():
    files = ["../data/androzoo/description-improvement/xin_sunil_shared_pkgs.txt",
             "../data/androzoo/description-improvement/xin_sunil_non_shared_pkgs.txt"]
    visited = set()
    with open("../data/androzoo/description-improvement/iot_pkgs_big_range.txt", 'a+') as des:
        for file in files:
            with open(file, 'r') as src:
                for line in src:
                    pkg_name = line.strip('\n')
                    if pkg_name not in visited:
                        print(pkg_name, file=des)
                    visited.add(pkg_name)
        df = pd.read_csv("../data/final_dataset/package_label_list.csv")
        for i, pkg_name in enumerate(df["pkg_name"]):
            if df["label"][i] == 1:
                if pkg_name not in visited:
                    print(pkg_name, file=des)
                visited.add(pkg_name)


def get_iot_apps():
    res = set()
    with open("../data/androzoo/description-improvement/xin_sunil_shared_pkgs.txt", 'r') as f:
        for line in f:
            res.add(line.strip('\n'))
    return res


def categorize_app():
    iot_apps = get_iot_apps()
    # df = pd.read_csv(save_path)
    types = []
    byte_sizes = []
    pkg_names = []
    sizes = []
    with open(save_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip('\n')
            pkg_name, cur_size = line.split(',', 1)
            pkg_names.append(pkg_name)
            sizes.append(cur_size)
            # cur_size = df["size"][i]
            if cur_size != "Varies with device":
                if ',' in cur_size:
                    cur_size = cur_size.replace(',', '')
                if cur_size.endswith('M'):
                    cur_size = float(cur_size[:-1])
                    byte_size = cur_size * 1000
                elif cur_size.endswith('k'):
                    byte_size = float(cur_size[:-1])
                elif cur_size.endswith('G'):
                    cur_size = float(cur_size[:-1])
                    byte_size = cur_size * 1000000
                else:
                    byte_size = None
            else:
                byte_size = None
            if pkg_name in iot_apps:
                cur_type = "IoT App"
            else:
                cur_type = "Non-IoT App"
            types.append(cur_type)
            byte_sizes.append(byte_size)
    df = pd.DataFrame({"package_name": pkg_names, "type": types, "size": sizes, "kb": byte_sizes})
    # df["type"] = types
    # df["kb"] = byte_sizes
    df.to_csv("data/apk_size/all_size_with_type.csv", index=False)


def box_plot():
    sns.set_theme(style="whitegrid")
    df = pd.read_csv("data/apk_size/all_size_with_type.csv")

    # IoT app
    df = df.loc[df['type'] == 'IoT App']
    ax = sns.violinplot(y="kb", data=df, palette="Set3")
    ax.set_yscale("log")
    ax.set(xlabel=None)
    ax.set(ylabel="File Size in KB")
    ax.set(title="IoT App File Size Distribution")

    # compare
    # ax = sns.violinplot(x="type", y="kb", data=df, palette="Set3")
    # # sns.stripplot(x="type", y="kb", data=df,
    # #               size=4, color=".3", linewidth=0)
    # ax.set_yscale("log")
    # ax.set(xlabel="IoT apps v.s. Non-IoT apps")
    # ax.set(ylabel="File Size in KB")
    # ax.set(title="App File Size Comparison")

    # plt.xlabel('IoT v.s. Non-IoT')
    # plt.xlabel("")
    # plt.ylabel('App file size')
    # sns.set_theme(style="whitegrid")
    # tips = sns.load_dataset("tips")
    # ax = sns.boxplot(x=tips["total_bill"])
    # g1.set(xticklabels=[])  # remove the tick labels
    # g1.set(title='Exercise: Pulse by Time for Exercise Type')  # add a title
    # g1.set(xlabel=None)  # remove the axis label
    plt.show()


if __name__ == '__main__':
    # get_all_sizes()
    # check_size_unit()
    # get_big_range_iot_pkgs()
    # categorize_app()
    box_plot()