#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: preprocess_final_dataset.py
@time: 3/22/21 11:10 PM
@desc:
"""
import json
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
import random

training_set_path = "../data/final_dataset/dataset_split/training_set.txt"
test_set_path = "../data/final_dataset/dataset_split/test_set.txt"


traditional_training_original_path = "../data/final_dataset/dataset_traditional/training_set_original.txt"
traditional_training_new_path = "../data/final_dataset/dataset_traditional/training_set.txt"
traditional_test_path = "../data/final_dataset/dataset_traditional/test_set.txt"
traditional_validation_path = "../data/final_dataset/dataset_traditional/validation_set.txt"

neural_nets_training_original_path = "../data/final_dataset/dataset_neural_networks/training_set_original.txt"
neural_nets_training_new_path = "../data/final_dataset/dataset_neural_networks/training_set.txt"
neural_nets_test_path = "../data/final_dataset/dataset_neural_networks/test_set.txt"
neural_nets_validation_path = "../data/final_dataset/dataset_neural_networks/validation_set.txt"

tp = TextProcessor("")


def process_traditional(file_path, file_save):
    with open(file_save, 'w+') as des:
        with open(file_path, 'r') as src:
            for line in src:
                js = json.loads(line)
                pkg_name = js["app_id"]
                description = js["description"]
                tp.text = description
                description_processed = tp.process(remove_stop_word=True, stem_words=True)
                label = int(js["label"])
                print(json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": label}), file=des)


def process_neural_nets(file_path, file_save):
    glove_model = glove_dictionary_load()
    with open(file_save, 'w+') as des:
        with open(file_path, 'r') as src:
            for line in src:
                js = json.loads(line)
                pkg_name = js["app_id"]
                description = js["description"]
                tp.text = description
                description_processed = tp.process(stem_words=False, use_model_filter=True,
                                                   model_embedding=glove_model)
                label = int(js["label"])
                print(json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": label}),
                      file=des)


def process_all():
    process_traditional(training_set_path, traditional_training_original_path)
    process_traditional(test_set_path, traditional_test_path)
    process_neural_nets(training_set_path, neural_nets_training_original_path)
    process_neural_nets(test_set_path, neural_nets_test_path)


def split_validation_set(training_original_path, training_new_path, validation_path):
    lines = open(training_original_path, 'r').read().strip().split('\n')
    num_samples = len(lines)
    all_index = list(range(0, num_samples))
    validation_index = random.sample(all_index, int(0.15*num_samples))
    validation_index = set(validation_index)
    with open(training_new_path, 'w+') as training:
        with open(validation_path, 'w+') as validation:
            for i, line in enumerate(lines):
                if i in validation_index:
                    print(line.strip('\n'), file=validation)
                else:
                    print(line.strip('\n'), file=training)


if __name__ == '__main__':
    split_validation_set(traditional_training_original_path, traditional_training_new_path, traditional_validation_path)
    split_validation_set(neural_nets_training_original_path, neural_nets_training_new_path, neural_nets_validation_path)