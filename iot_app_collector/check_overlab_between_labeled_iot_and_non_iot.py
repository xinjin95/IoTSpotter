#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: check_overlab_between_labeled_iot_and_non_iot.py
@time: 3/16/21 10:38 AM
@desc:
"""
import json
from fuzzywuzzy import fuzz

xxx_first_annotation_path = "../data/sp19_dataset/result/annotation_english_result_checked.txt"
xxx_second_annotation_path = "../data/iot_annotation/annotation_from_above_3.txt"

xxx_first_annotation_path = "../data/sp19_dataset/result/xxx_labels_checked.json"
xxx_second_annotation_path = "../data/iot_annotation/xxx_dataset_from_above_3.json"
non_iot_20K_dataset_path = "../data/androzoo/20k_metadata.json"
non_iot_xxx_path = "../data/non_iot_annotation/xxx_dataset.txt"
non_iot_xxx_path = "../data/non_iot_annotation/xxx_dataset.txt"

def load_xxx_pkgs(file_path):
    res = set()
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            label = js["label"]
            label = int(label)
            if label == 1:
                res.add(pkg_name)
    return res


def load_xxx_pkgs(file_path):
    input_file = open(file_path)
    # js = json.loads(file_path)
    pkgs = json.load(input_file)
    res = set()
    for pkg in pkgs:
        if 'app_id' in pkg.keys():
            pkg_name = pkg['app_id']
            # res.add()
        else:
            pkg_name = pkg["pkg_name"]
            # res.add(pkg["pkg_name"])
        label = pkg["label"]
        if label == "1":
            res.add(pkg_name)
        # print(label)
    # print("")

    return res


def get_all_labeled_iot():
    res = set()
    res = res.union(load_xxx_pkgs(xxx_first_annotation_path))
    res = res.union(load_xxx_pkgs(xxx_second_annotation_path))
    res = res.union(load_xxx_pkgs(xxx_first_annotation_path))
    res = res.union(load_xxx_pkgs(xxx_second_annotation_path))
    return res


def check_non_iot_and_iot_duplications():
    dids = get_all_labeled_iot()
    descriptions = set()
    with open(non_iot_xxx_path, 'w+') as xxx_file:
        with open(non_iot_xxx_path, 'w+') as xxx_file:
            with open(non_iot_20K_dataset_path, 'r') as file:
                for i, line in enumerate(file):
                    js = json.loads(line)
                    pkg_name = js["app_id"]
                    description = js["description"]
                    if description in descriptions:
                        continue
                    descriptions.add(description)
                    if pkg_name in dids:
                        # print(pkg_name)
                        continue
                    if i < 10000:
                        print(json.dumps(js), file=xxx_file)
                    else:
                        print(json.dumps(js), file=xxx_file)


def fuzzy_text_similarity_calculation(threshold):
    dids = get_all_labeled_iot()
    descriptions = set()

    with open(non_iot_20K_dataset_path, 'r') as file:
        for i, line in enumerate(file):
            print(i)
            js = json.loads(line)
            pkg_name = js["app_id"]
            description = js["description"]
            if description in descriptions or pkg_name in dids:
                continue
            # descriptions.add(description)
            flag = True
            for d in descriptions:
                if fuzz.ratio(d, description) > threshold:
                    flag = False
                    print("*************** same here ************************")
                    print(d)
                    print("------------------------------------")
                    print(description)
                    break
            if flag:
                descriptions.add(description)
                if i < 2000:
                    with open(non_iot_xxx_path, 'a+') as xxx_file:
                        print(json.dumps(js), file=xxx_file)
                else:
                    with open(non_iot_xxx_path, 'a+') as xxx_file:
                        print(json.dumps(js), file=xxx_file)


if __name__ == '__main__':
    # res = set()
    # res = res.union(load_xxx_pkgs(xxx_first_annotation_path))
    # res = res.union(load_xxx_pkgs(xxx_second_annotation_path))
    # res = res.union(load_xxx_pkgs(xxx_first_annotation_path))
    # res = res.union(load_xxx_pkgs(xxx_second_annotation_path))
    # print(len(res))
    # check_non_iot_and_iot_duplications()
    fuzzy_text_similarity_calculation(threshold=80)