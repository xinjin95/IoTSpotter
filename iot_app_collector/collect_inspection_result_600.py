#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_inspection_result_600.py
@time: 4/6/21 10:57 AM
@desc:
"""
import pandas as pd
import json

sunil_annoataion_path = "../data/androzoo/random_300.json"
xin_annotation_path = "../data/androzoo/iot_classification_inspection - unshared_inspection_csv.csv"
metadata_original_path = "../data/androzoo/600_inspection/600_metadata_original.txt"
metadata_save_path = "../data/androzoo/600_inspection/600_metadata_with_label.txt"


def collect_annotated_list():
    labels = []
    app_ids = []
    sources = []
    df = pd.read_csv(xin_annotation_path)
    app_ids += list(df["pkg_name"])
    with open(sunil_annoataion_path, 'r') as f:
        data = json.load(f)
        for js in data:
            app_ids.append(js["id"])
    app_ids = set(app_ids)
    with open("../data/androzoo/600_inspection/pkgs.txt", 'w+') as des:
        for app in app_ids:
            print(app, file=des)


def add_label():
    app_dict = {}
    df = pd.read_csv(xin_annotation_path)
    for i, app_id in enumerate(df["pkg_name"]):
        label = df["manual_label"][i]
        label = int(label)
        source = df["Source"][i]
        source = str(source)
        app_dict[app_id] = {"label": label, "source": source}
    with open(sunil_annoataion_path, 'r') as f:
        data = json.load(f)
        for js in data:
            app_id = js["id"]
            label = js["label"]
            label = int(label)
            # if label != 0 and label != 1:
            #     print(label)
            source = "shared"
            app_dict[app_id] = {"label": label, "source": source}
    print(app_dict)
    file_save = open(metadata_save_path, 'a+')
    with open(metadata_original_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            app_id = js["app_id"]
            label = app_dict[app_id]["label"]
            source = app_dict[app_id]["source"]
            if label == -1:
                label = 0
            js["label"] = label
            js["source"] = source
            print(json.dumps(js), file=file_save)


if __name__ == '__main__':
    add_label()