#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: utility.py
@time: 2/9/21 11:40 AM
@desc:
"""

import json
import numpy as np


def load_data_set(path_file):
    texts = []
    labels = []
    with open(path_file, 'r') as file:
        for line in file:
            line = line.strip("\n")
            js = json.loads(line)
            texts.append(js["text"])
            labels.append(js["label"])
    labels = np.asarray(labels, dtype=np.int)
    return texts, labels


def load_data_set_by_label(path_file, target_label):
    texts = []
    labels = []
    with open(path_file, 'r') as file:
        for line in file:
            line = line.strip('\n')
            js = json.loads(line)
            if int(js["label"]) == target_label:
                texts.append(js["text"])
                labels.append(js["label"])
    labels = np.asarray(labels, dtype=np.int)
    return texts, labels
