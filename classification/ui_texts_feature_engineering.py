#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: ui_texts_feature_engineering.py
@time: 4/15/21 7:00 PM
@desc:
"""
import json

import pandas as pd
import os
from iot_app_collector.text_processor import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

iot_dir = "/home/xin/Documents/code/python/iot-measure/data/training_ui_info/iot/"
non_iot_dir = "/home/xin/Documents/code/python/iot-measure/data/training_ui_info/non_iot/"

tp = TextProcessor("")


def get_texts(folder):
    _, _, filenames = next(os.walk(folder))
    result = []
    for file_name in filenames:
        with open(folder + file_name, 'r') as file:
            for line in file:
                js = json.loads(line)
                UIs = js["UIs"]
                texts = []
                for xml, UI in UIs.items():
                    for widget in UI:
                        if "text" in widget.keys():
                            text = widget["text"]
                            texts.append(text)
                texts = " ".join(texts)
                tp.text = texts
                texts = tp.process()
                result.append(texts)
                # print(texts)
    return result


def get_sorted_dict(keys, values):
    from classification.dictionary import Dictionary
    res = {}
    for i, key in enumerate(keys):
        value = values[i]
        res[key] = value
    res = Dictionary(res)
    res = res.sort_by_value(decreasing_order=True)
    return res


if __name__ == '__main__':
    iot_texts = get_texts(iot_dir)
    non_iot_texts = get_texts(non_iot_dir)

    num_features = 1000
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3))
    score = tfidf_converter.fit_transform(iot_texts).toarray().sum(axis=0)/len(iot_texts)
    iot_keywords = tfidf_converter.get_feature_names()
    res_iot = get_sorted_dict(iot_keywords, score)
    print(iot_keywords)

    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3))
    score = tfidf_converter.fit_transform(non_iot_texts).toarray().sum(axis=0)/len(non_iot_texts)
    non_iot_keywords = tfidf_converter.get_feature_names()
    res_non_iot = get_sorted_dict(non_iot_keywords, score)
    print(non_iot_keywords)

    df = pd.DataFrame({"iot_keyword": list(res_iot.keys()), "iot_tf_idf_avg": list(res_iot.values()),
                       "non_iot_keyword": list(res_non_iot.keys()), "non_iot_tf_idf_avg": list(res_non_iot.values())})
    # df.to_csv("/home/xin/Documents/code/python/iot-measure/review_crawler/data/iot_UI_keywords.csv", index=False)

    counter_vector = CountVectorizer(ngram_range=(1, 3), vocabulary=list(set(iot_keywords).difference(set(non_iot_keywords))))
    score = counter_vector.fit_transform(iot_texts).toarray()
    for i in range(len(score)):
        for j in range(len(score[0])):
            if score[i][j] > 0:
                score[i][j] = 1
    score = score.sum(axis=0)

    iot_keywords = counter_vector.get_feature_names()
    print(len(iot_keywords))
    print(score)
    print("# of iot:", len(iot_texts))
    res = get_sorted_dict(iot_keywords, score)
    for i in res.keys():
        print(i)
    for i in res.values():
        print(i)