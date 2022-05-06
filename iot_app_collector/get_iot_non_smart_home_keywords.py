#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_iot_non_smart_home_keywords.py
@time: 3/12/21 10:40 AM
@desc:
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from iot_app_collector.text_processor import TextProcessor

data_path = "../data/sp19_dataset/result/non_smart_home.txt"

texts = []
tp = TextProcessor("")
with open(data_path, 'r') as file:
    for line in file:
        js = json.loads(line)
        tp.text = js["description"]
        res = tp.process()
        texts.append(res)

num_features = 300
tf_idf_converter = tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
tfidf_converter.fit(texts)
print(tf_idf_converter.get_feature_names())