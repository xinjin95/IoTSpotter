#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_non_iot_1K.py
@time: 4/26/21 5:41 PM
@desc:
"""
import json
import pandas as pd
import random
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
from nltk.tokenize.toktok import ToktokTokenizer

training_ui_path = "../data/ui_text_dataset/neural_net/training_set.txt"
non_iot_apps = set()

def sample_dataset():
    lines = []
    count_iot = 0
    with open(training_ui_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            label = js["label"]
            # pkg_name = js["pkg_name"]
            if label == 0:
                lines.append(js)
    target = random.sample(lines, 1050)
    pkgs = []
    texts = []
    labels = []
    tp = TextProcessor("")
    model = glove_model = glove_dictionary_load()
    for js in target:
        pkg_name = js["pkg_name"]
        # print(pkg_name)
        text = js["text"]
        tp.text = text
        text = tp.process(stem_words=True)
        tokens = ToktokTokenizer().tokenize(text)
        if len(tokens) > 10:
            non_iot_apps.add(pkg_name)
        # label = int(js["label"])
        # if label == 1:
        #     count_iot += 1
        # pkgs.append(pkg_name)
        # texts.append(text)
        # labels.append(label)
    # df = pd.DataFrame.from_dict({"ui_text": texts, "label": labels, "pkg_name": pkgs})
    # df.to_csv(csv_path, index=False)
    # print(count_iot)
    # print(len(labels)-count_iot)


def record_non_iot_apps():
    non_iot_path = "../data/ui_text_dataset/annotation/result/non_iot_app_list.txt"
    with open(non_iot_path, 'w+') as file:
        for app in non_iot_apps:
            print(app, file=file)


if __name__ == '__main__':
    sample_dataset()
    print(len(non_iot_apps))
    record_non_iot_apps()