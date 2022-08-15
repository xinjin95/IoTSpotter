#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: calculate_install.py
@time: 8/19/21 6:08 PM
@desc:
"""
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from calculate_rate import get_attribute, iot_app_metadata_path

save_path = "data/installs/iot_installs.csv"


def get_installs():
    attr_name = "installs"
    get_attribute(iot_app_metadata_path, save_path, attr_name)


def process_installs():
    install_nums = []
    df = pd.read_csv(save_path)
    for install in df["installs"]:
        install = int(install.replace(',', '').replace('+', ''))
        install_nums.append(install)
    df["install_num"] = install_nums
    df.to_csv(save_path, index=False)


def box_plot():
    df = pd.read_csv(save_path)
    sns.set_theme(style="whitegrid")

    ax = sns.boxplot(y="install_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    ax.set_yscale("log")
    ax.set(ylabel="Download Number")
    ax.set(title="IoT App Download Number Distribution")
    plt.show()


def violin_plot():
    df = pd.read_csv(save_path)
    sns.set_theme(style="whitegrid")

    ax = sns.violinplot(y="install_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    ax.set_yscale("log")
    ax.set(ylabel="Download Number")
    ax.set(title="IoT App Download Number Distribution")
    plt.show()


if __name__ == '__main__':
    # get_installs()

    # process_installs()
    violin_plot()