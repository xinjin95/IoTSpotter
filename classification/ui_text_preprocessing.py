#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: ui_text_preprocessing.py
@time: 4/19/21 10:45 AM
@desc:
"""
import json
import os
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load


training_apps = set()
validation_apps = set()
testing_apps = set()
empty_ui_texts = []
no_static_uis = []

training_set_path = "../data/final_dataset/dataset_traditional/training_set.txt"
validation_set_path = "../data/final_dataset/dataset_traditional/validation_set.txt"
testing_set_path = "../data/final_dataset/dataset_traditional/test_set.txt"


iot_dir = "/home/xin/Documents/code/python/iot-measure/data/training_ui_info/iot/"
non_iot_dir = "/home/xin/Documents/code/python/iot-measure/data/training_ui_info/non_iot/"


def get_sets(file_path, app_set):
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            app_set.add(pkg_name)


def collect_apps():
    get_sets(training_set_path, training_apps)
    get_sets(validation_set_path, validation_apps)
    get_sets(testing_set_path, testing_apps)
    print(len(training_apps), len(validation_apps), len(testing_apps))


def get_dataset(folder, label):

    tp = TextProcessor("")
    _, _, filenames = next(os.walk(folder))
    print(len(filenames))
    glove_model = glove_dictionary_load()
    file_training = open("../data/ui_text_dataset/traditional/training_set.txt", 'a+')
    file_validation = open("../data/ui_text_dataset/traditional/validation_set.txt", 'a+')
    file_testing = open("../data/ui_text_dataset/traditional/test_set.txt", 'a+')
    # file_training = open("../data/ui_text_dataset/neural_net/training_set.txt", 'a+')
    # file_validation = open("../data/ui_text_dataset/neural_net/validation_set.txt", 'a+')
    # file_testing = open("../data/ui_text_dataset/neural_net/test_set.txt", 'a+')
    for file_name in filenames:
        with open(folder + file_name, 'r') as file:
            for line in file:
                line = line.strip('\n')
                # try:
                #     js = json.loads(line)
                # except:
                #     print(line)
                #     js = None
                # if js is None:
                #     continue
                js = json.loads(line)
                UIs = js["UIs"]
                # print(len(UIs))
                if len(UIs) == 0:
                    no_static_uis.append(pkg_name)
                pkg_name = js["appName"]
                texts = []
                for xml, UI in UIs.items():
                    for widget in UI:
                        if "text" in widget.keys():
                            text = widget["text"]
                            texts.append(text)
                texts = " ".join(texts)
                if texts == "":
                    empty_ui_texts.append(pkg_name)
                    # print(pkg_name, empty_ui_texts)
                    continue
                tp.text = texts

                # for traditional dataset collection
                texts = tp.process()

                # for neural nets
                # texts = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)

                if pkg_name in training_apps:
                    print(json.dumps({"pkg_name": pkg_name, "text": texts, "label": label}), file=file_training)
                elif pkg_name in validation_apps:
                    print(json.dumps({"pkg_name": pkg_name, "text": texts, "label": label}), file=file_validation)
                elif pkg_name in testing_apps:
                    print(json.dumps({"pkg_name": pkg_name, "text": texts, "label": label}), file=file_testing)


def collect_dataset():
    collect_apps()
    get_dataset(iot_dir, label=1)
    get_dataset(non_iot_dir, label=0)
    print(len(empty_ui_texts))
    print(len(no_static_uis))


if __name__ == '__main__':
    collect_dataset()