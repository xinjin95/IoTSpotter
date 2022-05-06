#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_permissions.py
@time: 8/20/21 5:27 PM
@desc:
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from classification.dictionary import Dictionary

manifest_path = "data/manifest_parse_result/merged_results.txt"

def get_permission():
    with open("data/permission/iot_app_permissions.txt", 'w+') as des:

        with open(manifest_path, 'r') as src:
            for i, line in enumerate(src):
                print(i)
                js = json.loads(line)
                pkg_name = js["packageName"]
                if "uses-permission" in js:
                    permissions = js["uses-permission"]
                else:
                    permissions = []

                if "permission" in js:
                    permissions += js["permission"]
                # permissions = list(set(permissions))
                js = {"app_name": pkg_name, "permission": permissions}
                print(json.dumps(js), file=des)


def calculate_permission():
    pkg_names = []
    permission_nums = []
    with open(manifest_path, 'r') as src:
        for i, line in enumerate(src):
            js = json.loads(line)
            pkg_name = js["packageName"]
            if "uses-permission" in js:
                permissions = js["uses-permission"]
            else:
                permissions = []

            if "permission" in js:
                permissions += js["permission"]
            permission_num = len(permissions)
            pkg_names.append(pkg_name)
            permission_nums.append(permission_num)
    df = pd.DataFrame({"package_name": pkg_names, "permission_num": permission_nums})
    df.to_csv("data/permission/permission_distribution.csv")


def box_plot():
    df = pd.read_csv("data/permission/permission_distribution.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.boxplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.boxplot(y="permission_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="Number of Permissions")
    ax.set(title="IoT App Permission Number Distribution")
    plt.show()


def violin_plot():
    df = pd.read_csv("data/permission/permission_distribution.csv")
    sns.set_theme(style="whitegrid")

    # ax = sns.boxplot(y="miniSdkVersion", data=df, palette="Set3")
    ax = sns.violinplot(y="permission_num", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    # ax.set_yscale("log")
    ax.set(ylabel="Number of Permissions")
    ax.set(title="IoT App Permission Number Distribution")
    plt.show()



if __name__ == '__main__':
    # calculate_permission()
    # violin_plot()
    get_permission()