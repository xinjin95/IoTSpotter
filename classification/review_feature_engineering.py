#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: review_feature_engineering.py
@time: 4/15/21 6:12 PM
@desc:
"""
import json

import pandas as pd

from iot_app_collector.text_processor import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# import pandas as pd

review_file_path = "/home/xxx/Documents/code/python/iot-measure/review_crawler/data/top_100_reviews_training.txt"

iot_texts = []
non_iot_texts = []

tp = TextProcessor("")

with open(review_file_path, 'r') as file:
    for i, line in enumerate(file):
        print(i)
        js = json.loads(line)
        label = js["label"]
        reviews = js["reviews"]
        if len(reviews) == 0:
            continue
        grouped_review = []
        for review in reviews:
            content = review["content"]
            if content is None:
                continue
            tp.text = content
            content = tp.process()
            # if label == 0:
            #     non_iot_texts.append(content)
            # else:
            #     iot_texts.append(content)
            grouped_review.append(content)
        grouped_review = " ".join(grouped_review)
        if label == 0:
            non_iot_texts.append(grouped_review)
        else:
            iot_texts.append(grouped_review)


def get_sorted_dict(keys, values):
    from classification.dictionary import Dictionary
    res = {}
    for i, key in enumerate(keys):
        value = values[i]
        res[key] = value
    res = Dictionary(res)
    res = res.sort_by_value(decreasing_order=True)
    return res

print("iot:", len(iot_texts))
print("non iot", len(non_iot_texts))

with open("/home/xxx/Documents/code/python/iot-measure/review_crawler/data/iot_reviews.txt", 'w+') as des:
    for iot_text in iot_texts:
        print(iot_text, file=des)

with open("/home/xxx/Documents/code/python/iot-measure/review_crawler/data/non_iot_reviews.txt", 'w+') as des:
    for non_iot_text in non_iot_texts:
        print(non_iot_text, file=des)

num_features = 1000
tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3))
score = tfidf_converter.fit_transform(iot_texts).toarray().sum(axis=0)/len(iot_texts)
iot_keywords = tfidf_converter.get_feature_names()
res_iot = get_sorted_dict(iot_keywords, score)
# counter = counter.toarray().sum(axis=0)
print(iot_keywords)
# print(counter)

tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3))
score = tfidf_converter.fit_transform(non_iot_texts).toarray().sum(axis=0)/len(non_iot_texts)
non_iot_keywords = tfidf_converter.get_feature_names()
res_non_iot = get_sorted_dict(non_iot_keywords, score)
print(non_iot_keywords)
# print(counter)

# df = pd.DataFrame({"iot_keyword": iot_keywords, "non_iot_keyword": non_iot_keywords})
df = pd.DataFrame({"iot_keyword": list(res_iot.keys()), "iot_tf_idf_avg": list(res_iot.values()),
                    "non_iot_keyword": list(res_non_iot.keys()), "non_iot_tf_idf_avg": list(res_non_iot.values())})
df.to_csv("/home/xxx/Documents/code/python/iot-measure/review_crawler/data/iot_reviews_keywords_grouped.csv", index=False)

counter_vector = CountVectorizer(ngram_range=(1, 3), vocabulary=list(set(iot_keywords).difference(set(non_iot_keywords))))
score = counter_vector.fit_transform(iot_texts).toarray()
for i in range(len(score)):
    for j in range(len(score[0])):
        if score[i][j] > 0:
            score[i][j] = 1
score = score.sum(axis=0)
iot_keywords = counter_vector.get_feature_names()
print(len(iot_keywords))
# print(score)
res = get_sorted_dict(iot_keywords, score)
for i in res.keys():
    print(i)
for i in res.values():
    print(i)