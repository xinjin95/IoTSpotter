#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: permission_feature_engineering.py
@time: 4/15/21 8:05 PM
@desc:
"""

import json

import pandas as pd
import os
from iot_app_collector.text_processor import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

iot_dir = "/home/xxx/Documents/code/python/iot-measure/data/training_ui_info/iot/"
non_iot_dir = "/home/xxx/Documents/code/python/iot-measure/data/training_ui_info/non_iot/"

tp = TextProcessor("")


def get_permissions(folder):
    _, _, filenames = next(os.walk(folder))
    result = []
    for file_name in filenames:
        with open(folder + file_name, 'r') as file:
            for line in file:
                js = json.loads(line)
                permissions = js["permissions"]
                permissions = [permission.lower() for permission in permissions]
                # permissions = " ".join(permissions)
                result.append(permissions)

    return result


def identity_tokenizer(text):
  return text


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
    iot_texts = get_permissions(iot_dir)
    non_iot_texts = get_permissions(non_iot_dir)

    num_features = 200
    tfidf_converter = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False, max_features=num_features,
                                      ngram_range=(1, 1))
    score = tfidf_converter.fit_transform(iot_texts).toarray().sum(axis=0)/len(iot_texts)
    iot_keywords = tfidf_converter.get_feature_names()
    res_iot = get_sorted_dict(iot_keywords, score)
    print(iot_keywords)
    print(len(iot_keywords))
    print(score)
    # for key, value in res.items():
    #     print(key, value)

    tfidf_converter = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False, max_features=num_features,
                                      ngram_range=(1, 1))
    score = tfidf_converter.fit_transform(non_iot_texts).toarray().sum(axis=0)/len(non_iot_texts)
    non_iot_keywords = tfidf_converter.get_feature_names()
    res_non_iot = get_sorted_dict(non_iot_keywords, score)
    print(non_iot_keywords)
    print(len(non_iot_keywords))
    print(score)

    print("iot specific:", len(list(set(iot_keywords).difference(set(non_iot_keywords)))), list(set(iot_keywords).difference(set(non_iot_keywords))))

    # df = pd.DataFrame({"iot_keyword": list(res_iot.keys()), "iot_tf_ief_avg": list(res_iot.values()),
    #                    "non_iot_keyword": list(res_non_iot.keys()), "non_iot_avg": list(res_non_iot.values())})
    # df.to_csv("/home/xxx/Documents/code/python/iot-measure/review_crawler/data/permission_keywords.csv",
    #           index=False)
    for permission in list(set(iot_keywords).difference(set(non_iot_keywords))):
        print(permission)
    counter_vector = CountVectorizer(tokenizer=identity_tokenizer, lowercase=False, vocabulary=list(set(iot_keywords).difference(set(non_iot_keywords))),
                                      ngram_range=(1, 1))
    score = counter_vector.fit_transform(iot_texts).toarray().sum(axis=0)
    iot_keywords = counter_vector.get_feature_names()
    print(len(iot_keywords))
    print(score)
    # for i in iot_keywords:
    #     print(i)
    # for i in score:
    #     print(i)
    res = get_sorted_dict(iot_keywords, score)
    for i in res.keys():
        print(i)
    for i in res.values():
        print(i)