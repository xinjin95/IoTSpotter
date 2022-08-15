#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: convert_metadata_csv.py
@time: 3/29/21 11:12 PM
@desc:
"""

import argparse
import pandas as pd
import json


def convert(metadata_path, save_path, target_label):
    pkgs = []
    descriptions = []
    labels = []
    titles = []
    with open(metadata_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            description = js["description"]
            title = js["title"]
            label = target_label
            pkgs.append(pkg_name)
            descriptions.append(description)
            labels.append(label)
            titles.append(title)
    df = pd.DataFrame({"description": descriptions, "title": titles, "manual_label": labels, "prediction": labels,
                       "pkg_name": pkgs})
    df.to_csv(save_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--metadata_path", type=str, required=True)
    parser.add_argument("-s", "--save_path", type=str, required=True)
    parser.add_argument("-l", "--label", type=int, required=True)

    args = parser.parse_args()

    metadata_path = args.metadata_path
    save_path = args.save_path
    label = args.label
    convert(metadata_path, save_path, label)