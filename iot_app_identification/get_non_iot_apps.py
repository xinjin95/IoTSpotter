#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_non_iot_apps.py
@time: 2/2/21 10:29 AM
@desc:
"""

import json
import pandas as pd
from iot_app_collector.text_processor import TextProcessor
from sklearn.feature_extraction.text import CountVectorizer


def get_from_2k_apps():
    non_iot_dir = "../data/non-iot-app/2k_apps.txt"
    csv = "../data/non_iot-app/2k_apps.csv"

    dids = set()
    des_file = open(csv, 'a+')

    with open(non_iot_dir, 'r') as file:
        ids = []
        descriptions = []
        developers = []
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            description = js["description"]
            developer = js["developer"]
            if developer not in dids:
                description = description.replace(',', ';').replace('\n', '\t')
                print("{},{},{}".format(pkg_name, description, developer), file=des_file)
            dids.add(developer)


def load_keywords() -> set:
    keywords = open("../data/keyword/bigram.txt", 'r').read().strip().split('\n')
    keywords += open("../data/keyword/trigram.txt", 'r').read().strip().split('\n')
    return set(keywords)


def filter_from_20K_apps():
    path_file = "../data/androzoo/20k_metadata.json"
    path_save = "../data/dataset/non_iot.txt"
    file_save = open(path_save, 'a+')
    file_contains = open("../data/dataset/non_iot_filter/contains.txt", 'a+')
    file_not_contains = open("../data/dataset/non_iot_filter/not_contains.txt", 'a+')
    keywords = load_keywords()
    tp = TextProcessor("")
    with open(path_file, 'r') as file:
        for i, line in enumerate(file):
            # if i > 1000:
            #     continue
            # if i != 1299:
            #     continue
            js = json.loads(line)
            pkg_name = js["app_id"]
            print("{}, {}".format(i, pkg_name))
            description = js["description"]
            tp.text = description
            description_processed = tp.process()
            # if len(description_processed) == 0:
            #     continue
            res = [description_processed]
            # print(res)
            # contains_keyword = False
            # for keyword in keywords:
            #     if keyword in res:
            #         contains_keyword = True
            try:
                vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 3))
                vectorizer.fit(res)
                grams = vectorizer.get_feature_names()
            except:
                continue
            contains_keyword = any(gram in keywords for gram in grams)
            if contains_keyword:
                matched_grams = ""
                for gram in grams:
                    if gram in keywords:
                        matched_grams = matched_grams + gram + ", "
                print(pkg_name + ":" + matched_grams, file=file_contains)
            else:
                print(pkg_name, file=file_not_contains)
                print(json.dumps({"pkg_name": pkg_name, "description": description_processed}), file=file_save)


if __name__ == '__main__':
    filter_from_20K_apps()
