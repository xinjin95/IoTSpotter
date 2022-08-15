#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: calculate_mini_sdk.py
@time: 8/19/21 10:57 PM
@desc:
"""
import glob
import json

import pandas as pd

root_dir = "data/manifest_parse_result/"
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def get_mini_sdk():
    pkg_names = []
    mini_sdks = []
    files = glob.glob(root_dir + '*')
    print("# of files:", len(files))
    for i, file in enumerate(files):
        with open(file, 'r') as f:
            for line in f:
                js = json.loads(line)
                pkg_name = js["packageName"]
                if "minSdkVersion" in js:
                    mini_sdk = js["minSdkVersion"]
                else:
                    mini_sdk = None
                print(i, pkg_name)
                pkg_names.append(pkg_name)
                mini_sdks.append(mini_sdk)
    df = pd.DataFrame({"package_name": pkg_names, "miniSdkVersion": mini_sdks})
    df.to_csv("data/mini_sdk/iot_mini_sdk.csv", index=False)


def get_both_sdk_version():
    pkg_names = []
    sdk_types = []
    sdks = []
    with open("data/manifest_parse_result/merged_results.txt", 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["packageName"]
            if "minSdkVersion" in js:
                mini_sdk = int(js["minSdkVersion"])
            else:
                mini_sdk = None
            if "targetSdkVersion" in js:
                target_sdk = int(js["targetSdkVersion"])
                if target_sdk > 30:
                    target_sdk = None
            else:
                target_sdk = None
            sdk_types.append("Minimal SDK Version")
            sdks.append(mini_sdk)
            sdk_types.append("Target SDK Version")
            sdks.append(target_sdk)
            print(i, pkg_name)
            pkg_names.append(pkg_name)
            pkg_names.append(pkg_name)
            # mini_sdks.append(mini_sdk)
    print(len(sdks), len(sdk_types))
    df = pd.DataFrame({"package_name": pkg_names, "SDK Type": sdk_types, "SDK Version": sdks})
    df.to_csv("data/mini_sdk/iot_sdk.csv", index=False)


def merge_manifest_parse_results():
    with open("data/manifest_parse_result/merged_results.txt", 'a+') as des:
        files = glob.glob(root_dir + '*')
        print("# of files:", len(files))
        for i, file in enumerate(files):
            print(i, file)
            if file == "data/manifest_parse_result/merged_results.txt":
                continue
            with open(file, 'r') as f:
                for line in f:
                    try:
                        js = json.loads(line)
                        print(json.dumps(js), file=des)
                    except:
                        print("error")


def box_plot():
    df = pd.read_csv("data/mini_sdk/iot_sdk.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.boxplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.boxplot(x="SDK Type", y="SDK Version", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="SDK Version")
    ax.set(title="IoT App SDK Version Distribution")
    plt.show()


def violin_plot():
    df = pd.read_csv("data/mini_sdk/iot_sdk.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.violinplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.violinplot(x="SDK Type", y="SDK Version", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="SDK Version")
    ax.set(title="IoT App SDK Version Distribution")
    # plt.rcParams.update({'font.size': 12})
    plt.rc('ytick', labelsize=20)
    plt.show()


if __name__ == '__main__':
    # get_mini_sdk()
    # merge_manifest_parse_results()
    violin_plot()
    # get_both_sdk_version()
    # box_plot()