#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: debug_logistic_model.py
@time: 4/19/21 9:06 PM
@desc:
"""

import json
import pandas as pd
import random


training_ui_path = "../data/ui_text_dataset/neural_net/training_set.txt"
csv_path = "../data/ui_text_dataset/annotation/all_1K.csv"


def sample_dataset():
    debug_path = "data/debug_logistic.csv"
    df = pd.read_csv(debug_path)
    used_apps = set(df["pkg_name"])
    lines = []
    count_iot = 0
    with open(training_ui_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            label = js["label"]
            pkg_name = js["pkg_name"]
            if label == 1 and pkg_name not in used_apps:
                lines.append(js)
    target = random.sample(lines, 1000)
    pkgs = []
    texts = []
    labels = []
    for js in target:
        pkg_name = js["pkg_name"]
        print(pkg_name)
        text = js["text"]
        label = int(js["label"])
        if label == 1:
            count_iot += 1
        pkgs.append(pkg_name)
        texts.append(text)
        labels.append(label)
    df = pd.DataFrame.from_dict({"ui_text": texts, "label": labels, "pkg_name": pkgs})
    df.to_csv(csv_path, index=False)
    print(count_iot)
    print(len(labels)-count_iot)


def split_dataset():
    all_1K_path = "../data/ui_text_dataset/annotation/all_1K.csv"
    xxx_path = "../data/ui_text_dataset/annotation/xxx.csv"
    xxx_path = "../data/ui_text_dataset/annotation/xxx.csv"
    df = pd.read_csv(all_1K_path)
    texts = []
    labels = []
    pkg_names = []
    for i, text in enumerate(df["ui_text"]):
        if i % 2 == 0:
            texts.append(text)
            labels.append(1)
            pkg_names.append(df["pkg_name"][i])
    df = pd.DataFrame.from_dict({"ui_text": texts, "label": labels, "pkg_name": pkg_names})
    df.to_csv(xxx_path, index=False)


if __name__ == '__main__':
    # sample_dataset()
    split_dataset()