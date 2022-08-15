#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: collect_final_dataset.py
@time: 3/22/21 3:37 PM
@desc:
"""
import json
import random
import pandas as pd

path_sp19_xxx = "../data/sp19_dataset/result/annotation_english_result_checked.txt"
# path_sp19_xxx_diff = ""
path_above3_xxx = "../data/iot_annotation/xxx_annotation_from_above_3_checked.txt"
path_non_iot_xxx = "../data/non_iot_annotation/result/xxx_dataset_annotation_confirmed.txt"

path_sp19_xxx = "../data/sp19_dataset/result/xxx_labels_checked.json"
# path_sp19_xxx_diff = ""
path_above3_xxx = "../data/iot_annotation/xxx_dataset_from_above_3_checked.json"
path_non_iot_xxx = "../data/non_iot_annotation/result/xxx_dataset_noniot_confirmed.json"

path_package_list_save = "../data/final_dataset/package_label_list.csv"
dids = set()


def xxx_annotation_result(file_path):
    with open(path_package_list_save, 'a+') as des:
        with open(file_path, 'r') as file:
            for line in file:
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                label = int(js["label"])
                if pkg_name in dids:
                    continue
                dids.add(pkg_name)
                if label == 0 or label == 1:
                    print("{},{}".format(pkg_name, label), file=des)


def xxx_annotation_result(file_path):
    src = open(file_path, 'r')
    lines = json.load(src)
    with open(path_package_list_save, 'a+') as des:
        for js in lines:
            pkg_name = ""
            if "app_id" in js.keys():
                pkg_name = js["app_id"]
            elif "pkg_name" in js.keys():
                pkg_name = js["pkg_name"]
            if pkg_name == "":
                continue
            label = js["label"]
            label = int(label)
            if pkg_name in dids:
                continue
            dids.add(pkg_name)
            if label == 1 or label == 0:
                print("{},{}".format(pkg_name, label), file=des)


def collect_all():
    xxx_annotation_result(path_sp19_xxx)
    xxx_annotation_result(path_above3_xxx)
    xxx_annotation_result(path_non_iot_xxx)
    xxx_annotation_result(path_sp19_xxx)
    xxx_annotation_result(path_above3_xxx)
    xxx_annotation_result(path_non_iot_xxx)


def check_status():
    df = pd.read_csv(path_package_list_save)
    labels = df["label"]
    print("num of 1 labels: {}".format(sum(labels)))
    print("num of 0 labels: {}".format(len(labels) - sum(labels)))

    num_zero = 0
    num_one = 0
    with open("../data/final_dataset/complete_dataset_metadata.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            label = js["label"]
            label = int(label)
            if label == 0:
                num_zero += 1
            elif label == 1:
                num_one += 1
    print("num of 1 labels: {}".format(num_one))
    print("num of 0 labels: {}".format(num_zero))


def split_dataset():
    df = pd.read_csv(path_package_list_save)
    labels = df["label"]
    num_samples = len(labels)
    all_index = list(range(0, num_samples))
    print(num_samples)
    testing_index = random.sample(all_index, int(num_samples*0.15))
    testing_index = set(testing_index)
    print(len(testing_index))
    path_training = "../data/final_dataset/dataset_split/training_set.txt"
    path_testing = "../data/final_dataset/dataset_split/test_set.txt"
    path_whole_dataset = "../data/final_dataset/complete_dataset_metadata.txt"
    with open(path_training, 'w+') as training:
        with open(path_testing, 'w+') as testing:
            with open(path_whole_dataset, 'r') as src:
                for i, line in enumerate(src):
                    js = json.loads(line)
                    if i in testing_index:
                        print(json.dumps(js), file=testing)
                    else:
                        print(json.dumps(js), file=training)


if __name__ == '__main__':
    # check_status()
    split_dataset()