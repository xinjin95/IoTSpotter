#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: check_iot_dataset.py
@time: 5/10/21 5:44 PM
@desc:
"""
import json
from text_processor import TextProcessor, glove_dictionary_load
import random

training_set1_path = "../data/androzoo/description-improvement/train_400_1.txt"
training_set2_path = "../data/androzoo/description-improvement/train_400_2.txt"
training_save_path = "../data/final_dataset/dataset_neural_networks/training_set.txt"
validation_save_path = "../data/final_dataset/dataset_neural_networks/validation_set.txt"


def check_apps(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            note = js["xxx_notes"]
            if len(note) != 0:
                print(js["description"])
                print(js["label"])
                print(js["app_id"])


tp = TextProcessor("")
glove_model = glove_dictionary_load()


def collect_dataset(file_path):
    file_training = open(training_save_path, 'a+')
    file_validation = open(validation_save_path, 'a+')
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            label = js["label"]
            description = js["description"]
            tp.text = description
            description = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)
            if random.random() > 0.75:
                print(json.dumps({"pkg_name": pkg_name, "description": description, "label": label}), file=file_validation)
            else:
                print(json.dumps({"pkg_name": pkg_name, "description": description, "label": label}),
                      file=file_training)

# check_apps(training_set1_path)
# check_apps(training_set2_path)


collect_dataset(training_set1_path)
collect_dataset(training_set2_path)