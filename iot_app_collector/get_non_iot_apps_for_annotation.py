#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_non_iot_apps_for_annotation.py
@time: 3/11/21 9:30 PM
@desc:
"""
import json
from iot_app_collector.text_processor import TextProcessor
from iot_app_identification.get_non_iot_apps import load_keywords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

metadata_20K_path = "../data/androzoo/20k_metadata.json"
xxx_path = "../data/non_iot_annotation/xxx_dataset.txt"
xxx_path = "../data/non_iot_annotation/xxx_dataset.txt"
csv_path = "../data/non_iot_annotation/annotation_csv.csv"


def split_dataset():
    with open(xxx_path, 'w+') as xxx_file:
        with open(xxx_path, 'w+') as xxx_file:
            with open(metadata_20K_path, 'r') as src:
                for i, line in enumerate(src):
                    js = json.loads(line)
                    if i < 10000:
                        print(json.dumps(js), file=xxx_file)
                    else:
                        print(json.dumps(js), file=xxx_file)


def build_dataset():
    descriptions = []
    pkgs = []
    labels = []
    tp = TextProcessor("")
    keywords = load_keywords()
    grams_list = []
    # xxx_path = "../data/re_annotation_trainingset/xxx_annotated.txt"
    xxx_path = "../data/validation/xxx.txt"
    with open(xxx_path, 'r') as file:
        for i, line in enumerate(file):
            print(i)
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
            label = js["classified_label"]
            descriptions.append(description)
            grams_list.append(matched_grams)
            pkgs.append(pkg_name)
            labels.append(label)
    df = pd.DataFrame({"description": descriptions, "keyword": grams_list, "label": labels, "pkg_name": pkgs})
    csv_path = "../data/validation/xxx_for_annotation.csv"
    df.to_csv(csv_path, index=False)


if __name__ == '__main__':
    build_dataset()