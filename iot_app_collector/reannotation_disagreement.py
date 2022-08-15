#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: reannotation_disagreement.py
@time: 11/8/21 2:03 PM
@desc:
"""
import pandas as pd


raw_path = "../data/re_annotation_trainingset/xxx_new_annotation_xxx_annotated.csv"

def get_app_disagreed(df):
    res = set()
    for i, label in enumerate(df["New Label"]):
        old_label = df["label"][i]
        if old_label != label:
            res.add(df["pkg_name"][i])
    return res

false_positive = ["com.kopa_android.UCam.plus", "com.vchecker.hudnav", "com.aaasurid.flightguideformavicair",
                  "com.muving", "com.paulino.haroldo.uiipademo"]
false_positive = set(false_positive)

def main():
    df = pd.read_csv(raw_path)
    apps = get_app_disagreed(df)
    for app in false_positive:
        apps.remove(app)
    # apps = apps.difference(false_positive)
    print("# of apps", len(apps))
    df = df[df["pkg_name"].isin(apps)]
    # print(df.head())
    df.to_csv("../data/re_annotation_trainingset/disagreement/xxx_disagree_with_xxx.csv", index=False)

if __name__ == '__main__':
    main()