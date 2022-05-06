#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: split_dataset.py
@time: 4/26/21 9:03 PM
@desc:
"""
from ui_text_classification.get_final_dataset import get_app_set
import random
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
import json

app_set = list(get_app_set())
validation_apps = random.sample(app_set, int(0.20 * len(app_set)))
training_apps = set(app_set).difference(set(validation_apps))
validation_apps = set(validation_apps)
# print(len(validation_apps))


def split_app(file_src, file_training, file_validation):
    file_training = open(file_training, 'a+')
    file_validation = open(file_validation, 'a+')
    tp = TextProcessor("")
    glove_model = glove_dictionary_load()
    with open(file_src, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            tp.text = js["text"]
            text = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)
            js["text"] = text
            if pkg_name in training_apps:
                print(json.dumps(js), file=file_training)
            elif pkg_name in validation_apps:
                print(json.dumps(js), file=file_validation)


if __name__ == '__main__':
    # traditional_src = "../data/ui_text_dataset/traditional/training_set.txt"
    # traditional_training = "data/dataset_traditional/training_set.txt"
    # traditional_validation = "data/dataset_traditional/validation_set.txt"
    # split_app(traditional_src, traditional_training, traditional_validation)
    neural_src = "../data/ui_text_dataset/neural_net/training_set.txt"
    neural_training = "data/dataset_neural_net/training_set.txt"
    neural_validation = "data/dataset_neural_net/validation_set.txt"
    split_app(neural_src, neural_training, neural_validation)