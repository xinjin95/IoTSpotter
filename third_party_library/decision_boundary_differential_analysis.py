#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: decision_boundary_differential_analysis.py
@time: 8/22/21 5:24 PM
@desc:
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

both_exist_path = "data/iot_specific_lib_filter/both_exist.csv"
only_iot_path = "data/iot_specific_lib_filter/only_in_iot.csv"


def cdf_count_both():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig, ax = plt.subplots(figsize=(4, 3))
    rcParams['axes.unicode_minus'] = False
    df = pd.read_csv(both_exist_path)
    sns.set_theme(style="whitegrid")
    ax = sns.ecdfplot(data=df, x="average_frequency_division",  stat="count", complementary=True)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel("Decision Boundary (" + r'$\mu$' + ")", fontsize=12)
    ax.set_ylabel('# Selected Package Names', fontsize=12)
    ax.set(yscale="log")
    ax.grid(axis="y")
    rcParams['ps.useafm'] = True
    rcParams['pdf.use14corefonts'] = True
    fig.set_tight_layout(True)
    plt.savefig("data/figures/both_exists_decision_boundary.pdf", format='pdf', dpi=500)
    plt.show()


def cdf_count_only():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig, ax = plt.subplots(figsize=(4, 3))
    rcParams['axes.unicode_minus'] = False
    df = pd.read_csv(only_iot_path)
    sns.set_theme(style="whitegrid")
    ax = sns.ecdfplot(data=df, x="iot_average_frequency", stat="count", complementary=True)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel("Decision Boundary (" + r'$\epsilon$' + ")", fontsize=12)
    ax.set_ylabel('# Selected Package Names', fontsize=12)
    ax.set(yscale="log")
    ax.grid(axis="y")
    rcParams['ps.useafm'] = True
    rcParams['pdf.use14corefonts'] = True
    fig.set_tight_layout(True)
    plt.savefig("data/figures/only_in_iot_decision_boundary.pdf", format='pdf', dpi=500)
    plt.show()


if __name__ == '__main__':
    cdf_count_only()
    # cdf_count_both()