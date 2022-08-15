#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_keywords.py
@time: 2/8/21 10:40 PM
@desc:
"""
import json
import re
from iot_app_collector.text_processor import TextProcessor

file_labelled_data = "../data/keyword/IoT-seed.txt"


def get_keywords():
    res = set()
    with open(file_labelled_data, 'r') as file:
        for line in file:
            js = json.loads(line)
            keyword = js["keywords"]
            for word in keyword:
                res.add(word)
    return res


def data_cleaner(sent):
    # Remove distracting single quotes
    lower_sent = sent.strip().lower()
    return re.sub("\'", "", lower_sent)


l_individidual_keywords = get_keywords()
s_individual_keywords = set(l_individidual_keywords)
print(len(s_individual_keywords))
d_keywords = {}
for m in s_individual_keywords:
    l_words = len(m.split())
    if l_words not in d_keywords:
        d_keywords[l_words] = [data_cleaner(m)]
    else:
        d_keywords[l_words].append(data_cleaner(m))


# bigram, trigram, 4 gram identification
print(len(d_keywords[1]))
print(len(d_keywords[2]))
print(len(d_keywords[3]))
print(len(d_keywords[4]))


def get_processed_bigram():
    remove_list = ["from anywhere", "control all", "on off,colors,dimming,timer,fade.jump,music"]
    updated_d_keywords = []
    for word in d_keywords[2]:
        if word not in remove_list:
            updated_d_keywords.append(word)
    tp = TextProcessor("")
    res = set()
    for word in updated_d_keywords:
        tp.text = word
        word_processed = tp.process()
        print("{}, {}".format(word, word_processed))
        res.add(word_processed)
    return res


def get_processed_trigram():
    tp = TextProcessor("")
    res = set()
    for word in d_keywords[3]:
        tp.text = word
        word_processed = tp.process()
        print("{}, {}".format(word, word_processed))
        res.add(word_processed)
    return res


def write2file(file_path, keywords):
    with open(file_path, 'w+') as file:
        for keyword in keywords:
            print(keyword, file=file)


# write2file("../data/keyword/bigram.txt", get_processed_bigram())
# write2file("../data/keyword/trigram.txt", get_processed_trigram())

print(len(get_processed_bigram()|get_processed_trigram()))