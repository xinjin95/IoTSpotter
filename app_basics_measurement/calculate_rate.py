#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: calculate_rate.py
@time: 8/19/21 5:41 PM
@desc:
"""
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

iot_app_metadata_path = "../data/androzoo/description-improvement/new_shared_37K_metadata.txt"
save_path = "data/rating/iot_rating.csv"

def get_attribute(metadata_path, save_path, attribute_name):
    package_names = []
    attr_values = []
    with open(metadata_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            attr_value = js[attribute_name]
            pkg_name = js["app_id"]
            package_names.append(pkg_name)
            attr_values.append(attr_value)
    df = pd.DataFrame({"package_name": package_names, attribute_name: attr_values})
    df.to_csv(save_path, index=False)


def get_rating():
    # save_path = "data/rating/iot_rating.csv"
    attr_name = "score"
    get_attribute(iot_app_metadata_path, save_path, attr_name)


def process_rating():
    df = pd.read_csv(save_path)
    num_rating = []
    for rating in df["score"]:
        print(float(rating))


def box_plot():
    df = pd.read_csv(save_path)
    sns.set_theme(style="whitegrid")
    ax = sns.boxplot(y="score", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    ax.set(ylabel="Scale 1 to 5")
    ax.set(title="IoT App Rating Distribution")
    plt.show()


def violin_plot():
    df = pd.read_csv(save_path)
    sns.set_theme(style="whitegrid")
    ax = sns.violinplot(y="score", data=df, palette="Set3")
    # sns.stripplot(y="score", data=df, size=2, color=".3", linewidth=0)
    ax.set(xlabel=None)
    ax.set(ylabel="Scale 1 to 5")
    ax.set(title="IoT App Rating Distribution")
    plt.show()


if __name__ == '__main__':
    # get_rating()
    # process_rating()
    # box_plot()
    violin_plot()