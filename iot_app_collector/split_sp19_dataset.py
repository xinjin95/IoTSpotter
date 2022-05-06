#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: split_sp19_dataset.py
@time: 3/5/21 1:32 PM
@desc:
"""
import json
import pandas as pd
from iot_app_identification.get_non_iot_apps import load_keywords
from iot_app_collector.text_processor import TextProcessor
from sklearn.feature_extraction.text import CountVectorizer

all_metadata_path = "../data/sp19_dataset/iot_app_metadata_sp19.txt"

sunil_path = "../data/sp19_dataset/sunil_dataset.txt"
app_list_path = "../data/sp19_dataset/app_list.txt"
# xin_path = "../data/sp19_dataset/xin_dataset.txt"
# csv_path = "../data/sp19_dataset/annotation_csv.csv"
# xin_path = "../data/iot_annotation/xin_dataset_from_above_3.txt"
# csv_path = "../data/iot_annotation/annotation_csv_from_above_3.csv"

xin_path = "../data/non_iot_annotation/xin_dataset.txt"
csv_path = "../data/non_iot_annotation/annotation_csv.csv"


def get_app_list():
    dids = set()
    with open(app_list_path, 'w+') as des:
        with open(all_metadata_path, 'r') as src:
            for line in src:
                line = line.strip('\n')
                js = json.loads(line)
                if js["app_id"] in dids:
                    print(js["app_id"])
                print(js["app_id"], file=des)
                dids.add(js["app_id"])


def split_dataset():
    xin_file = open(xin_path, 'a+')
    sunil_file = open(sunil_path, 'a+')
    with open(all_metadata_path, 'r') as src:
        for i, line in enumerate(src):
            line = line.strip('\n')
            if i < 787:
                print(line, file=sunil_file)
            else:
                print(line, file=xin_file)


def build_dataset():
    descriptions = []
    pkgs = []
    labels = []
    tp = TextProcessor("")
    keywords = load_keywords()
    grams_list = []
    with open(xin_path, 'r') as file:
        for i, line in enumerate(file):
            if i > 2000:
                continue
            js = json.loads(line)
            description = js['description']
            description = description.replace(',', ' ')
            tp.text = description
            description_processed = tp.process(stem_words=True)
            try:
                vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 3))
                vectorizer.fit([description_processed])
                grams = vectorizer.get_feature_names()
            except:
                grams = []
            contains_keyword = any(gram in keywords for gram in grams)
            matched_grams = ""
            if contains_keyword:
                # matched_grams = ""
                for gram in grams:
                    if gram in keywords:
                        matched_grams = matched_grams + gram + "\n"
            pkg_name = js['app_id']
            # pkg_name = js['pkg_name']
            # label = 1
            label = 0
            descriptions.append(description)
            grams_list.append(matched_grams)
            pkgs.append(pkg_name)
            labels.append(label)
    df = pd.DataFrame({"description": descriptions, "keyword": grams_list, "label": labels, "pkg_name": pkgs})
    df.to_csv(csv_path, index=False)


if __name__ == '__main__':
    # get_app_list()
    # split_dataset()
    build_dataset()