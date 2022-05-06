#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_activity.py
@time: 8/20/21 5:34 PM
@desc:
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from classification.dictionary import Dictionary

manifest_path = "data/manifest_parse_result/merged_results.txt"


def calculate_activity():
    pkg_names = []
    activity_nums = []
    with open(manifest_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["packageName"]
            if "activity" in js:
                activity = js["activity"]
            else:
                activity = []
            activity_num = len(activity)
            pkg_names.append(pkg_name)
            activity_nums.append(activity_num)
    df = pd.DataFrame({"package_name": pkg_names, "activity_num": activity_nums})
    df.to_csv("data/activity/activity_distribution.csv")


def box_plot():
    df = pd.read_csv("data/activity/activity_distribution.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.boxplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.boxplot(y="activity_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="Number of Activities")
    ax.set(title="IoT App Activity Number Distribution")
    plt.show()


def violin_plot():
    df = pd.read_csv("data/activity/activity_distribution.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.boxplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.violinplot(y="activity_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="Number of Activities")
    ax.set(title="IoT App Activity Number Distribution")
    plt.show()


if __name__ == '__main__':
    # calculate_activity()
    # box_plot()
    violin_plot()