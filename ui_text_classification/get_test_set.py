#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_test_set.py
@time: 4/26/21 10:55 PM
@desc:
"""
import json
import os
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
from nltk.tokenize.toktok import ToktokTokenizer

test_apps_metadata = "../data/androzoo/600_inspection/600_metadata_with_label.txt"
iot_apps = set()
non_iot_apps = set()


def get_apps():
    with open(test_apps_metadata, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            label = int(js["label"])
            if label==0:
                non_iot_apps.add(pkg_name)
            elif label == 1:
                iot_apps.add(pkg_name)


def collect_dataset():
    res = 0
    tp = TextProcessor("")
    folder = "../data/600_ui_info/"
    _, _, filenames = next(os.walk(folder))
    glove_model = glove_dictionary_load()
    file_testing = open("data/dataset_traditional/test_set.txt", 'a+')
    for file_name in filenames:
        with open(folder + file_name, 'r') as file:
            for line in file:
                line = line.strip('\n')
                js = json.loads(line)
                pkg_name = js["appName"]
                UIs = js["UIs"]
                if pkg_name in iot_apps:
                    label = 1
                elif pkg_name in non_iot_apps:
                    label = 0
                texts = []
                for xml, UI in UIs.items():
                    for widget in UI:
                        if "text" in widget.keys():
                            text = widget["text"]
                            texts.append(text)
                texts = " ".join(texts)
                if texts == "":
                    continue
                texts_original = texts
                tp.text = texts

                texts = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)
                tokens = ToktokTokenizer().tokenize(texts)
                if len(tokens) > 10:
                    res += label
                    print(json.dumps({"pkg_name": pkg_name, "text": texts, "label": label}), file=file_testing)
                    print(res)


if __name__ == '__main__':
    get_apps()
    collect_dataset()
