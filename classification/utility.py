#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
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
            texts.append(js["description"])
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
                texts.append(js["description"])
                labels.append(js["label"])
    labels = np.asarray(labels, dtype=np.int)
    return texts, labels
