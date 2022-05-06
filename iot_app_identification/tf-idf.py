#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: tf-idf.py
@time: 2/2/21 12:16 AM
@desc:
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from collections import Counter


def load_corpus(path_file):
    texts = []
    keywords = []
    with open(path_file, 'r') as file:
        for line in file:
            line = line.strip("\n")
            js = json.loads(line)
            texts.append(js["description"])
            keywords.append(js["keywords"])
    return texts, keywords


def analyze_keyword():
    path_iot_seed = "../data/keyword/IoT-seed.txt"
    _, keywords = load_corpus(path_iot_seed)
    counter = Counter()
    total = 0
    for words in keywords:
        for word in words:
            word = word.lower()
            counter[word] += 1
            total += 1
    print(total)
    print(len(counter.keys()))
    print(counter.most_common(10))


def tf_idf():
    path_iot_seed = "../data/keyword/IoT-seed.txt"
    descriptions, keywords = load_corpus(path_iot_seed)
    num_feature = 100
    tfidf_converter = TfidfVectorizer(max_features=num_feature, ngram_range=(2, 3))
    tfidf_converter.fit(descriptions)
    print(tfidf_converter.get_feature_names())


if __name__ == '__main__':
    # analyze_keyword()
    tf_idf()