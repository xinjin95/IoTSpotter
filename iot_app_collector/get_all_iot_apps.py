#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: get_all_iot_apps.py
@time: 2/22/21 2:23 PM
@desc:
"""
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
import json
import random

path_iot_apps = "../data/iot-app/full-6861-possible-smarthome.txt"
path_all_iot_apps = "../data/iot-app/all_keyword_filtered_apps.txt"


# file_save = open(path_all_iot_apps, 'a+')


def collect_iot_apps():
    tp = TextProcessor("")
    with open(path_all_iot_apps, 'w+') as file_save:
        with open(path_iot_apps, 'r') as file:
            for line in file:
                pkg_name, description = line.split("|||", 1)
                # print(pkg_name)
                # print(description)
                # print()
                tp.text = description
                description_processed = tp.process()
                print(json.dumps({"pkg_name": pkg_name, "description": description_processed}), file=file_save)


def build_corpus_neural_nets():
    tp = TextProcessor("")
    glove_model = glove_dictionary_load()
    path_large_training = "../data/dataset/training_large.txt"
    path_large_testing = "../data/dataset/testing_large.txt"
    training_apps = get_apps(path_large_training)
    testing_apps = get_apps(path_large_testing)
    # path_large_training = "../data/dataset/neural_nets_corpus/training_large_neural_nets.txt"
    # path_large_testing = "../data/dataset/neural_nets_corpus/testing_large_neural_nets.txt"
    path_large_training = "../data/dataset/neural_nets_corpus/training_large_original.txt"
    path_large_testing = "../data/dataset/neural_nets_corpus/testing_large_original.txt"
    path_all_non_iot = "../data/androzoo/20k_metadata.json"
    dids = set()
    with open(path_large_training, 'w+') as file_training:
        with open(path_large_testing, 'w+') as file_testing:
            with open(path_iot_apps, 'r') as file:
                for line in file:
                    pkg_name, description = line.split("|||", 1)
                    # tp.text = description
                    # description_processed = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)
                    # sample = json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": 1})
                    sample = json.dumps({"pkg_name": pkg_name, "description": description, "label": 1})
                    if pkg_name in dids:
                        continue
                    if pkg_name in training_apps:
                        print(sample, file=file_training)
                    elif pkg_name in testing_apps:
                        print(sample, file=file_testing)
                    dids.add(pkg_name)

            with open(path_all_non_iot, 'r') as file:
                for line in file:
                    js = json.loads(line)
                    pkg_name = js['app_id']
                    description = js['description']
                    # tp.text = description
                    # description_processed = tp.process(stem_words=False, use_model_filter=True,
                    #                                    model_embedding=glove_model)
                    # sample = json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": 0})
                    sample = json.dumps({"pkg_name": pkg_name, "description": description, "label": 0})
                    if pkg_name in dids:
                        continue
                    if pkg_name in training_apps:
                        print(sample, file=file_training)
                    elif pkg_name in testing_apps:
                        print(sample, file=file_testing)
                    dids.add(pkg_name)


def enlarge_training_set():
    tp = TextProcessor("")
    glove_model = glove_dictionary_load()
    path_large_training = "../data/dataset/training_large.txt"
    path_large_testing = "../data/dataset/testing_large.txt"
    training_apps = get_apps(path_large_training)
    testing_apps = get_apps(path_large_testing)
    used_apps = training_apps.union(testing_apps)
    non_iot_path = "../data/dataset/non_iot.txt"
    non_iot_apps = get_apps(non_iot_path)
    unused_iot_apps = non_iot_apps.difference(used_apps)
    print(len(unused_iot_apps))
    path_large_training = "../data/dataset/neural_nets_corpus/training_validation_large_set.txt"
    path_all_non_iot = "../data/androzoo/20k_metadata.json"
    # dids = set()
    with open(path_large_training, 'w+') as file_training:
        with open(path_all_non_iot, 'r') as file:
            for line in file:
                js = json.loads(line)
                pkg_name = js['app_id']
                description = js['description']
                tp.text = description
                description_processed = tp.process(stem_words=False, use_model_filter=True,
                                                   model_embedding=glove_model)
                sample = json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": 0})
                if pkg_name in used_apps:
                    continue
                if pkg_name in unused_iot_apps:
                    print(sample, file=file_training)
                used_apps.add(pkg_name)

        # total_iot_apps = 0
        new_iot_apps = get_new_iot_apps(used_apps, len(unused_iot_apps))
        for app in new_iot_apps:
            pkg_name = app["pkg_name"]
            description = app['description']
            tp.text = description
            description_processed = tp.process(stem_words=False, use_model_filter=True,
                                               model_embedding=glove_model)
            sample = json.dumps({"pkg_name": pkg_name, "description": description_processed, "label": 1})
            print(sample, file=file_training)


def get_new_iot_apps(used_apps, len_non_iot):
    import pandas as pd
    iot_files = ["keyword_device-names.csv", "keyword_protocols.csv", "keyword_smarthome.csv",
                 "keyword_managers.csv", "keyword_regex.csv"]
    iot_folder = "/home/xxx/Downloads/keywords/"

    new_iot_samples = []
    for file in iot_files:
        df = pd.read_csv(iot_folder+file)
        for i, pkg_name in enumerate(df['app_id']):
            if pkg_name not in used_apps:
                new_iot_samples.append({"pkg_name": pkg_name, "description": df['description'][i]})
            used_apps.add(pkg_name)
    return random.sample(new_iot_samples, len_non_iot)


def get_apps(path_file):
    res = set()
    with open(path_file, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            res.add(pkg_name)
    return res

def build_dataset():
    seed_list = list(range(6861))
    iot_index_training = random.sample(seed_list, int(len(seed_list) * 0.8))
    iot_index_training = set(iot_index_training)
    # print(len(iot_index_training))
    seed_list = list(range(19452))
    non_iot_index = random.sample(seed_list, 6861)
    non_iot_index_training = random.sample(non_iot_index, int(len(non_iot_index) * 0.8))
    non_iot_index_training = set(non_iot_index_training)
    non_iot_index_testing = [i for i in non_iot_index if i not in non_iot_index_training]
    non_iot_index_testing = set(non_iot_index_testing)

    path_large_training = "../data/dataset/training_large.txt"
    path_large_testing = "../data/dataset/testing_large.txt"
    with open(path_large_training, 'w+') as file_training:
        with open(path_large_testing, 'w+') as file_testing:
            iot_samples = open("../data/iot-app/all_keyword_filtered_apps.txt").read().strip().split('\n')
            for i, sample in enumerate(iot_samples):
                sample = sample.strip('\n')
                js = json.loads(sample)
                js["label"] = 1
                sample = json.dumps(js)
                if i in iot_index_training:
                    print(sample, file=file_training)
                else:
                    print(sample, file=file_testing)

            non_iot_samples = open("../data/dataset/non_iot.txt").read().strip().split('\n')
            for i, sample in enumerate(non_iot_samples):
                sample = sample.strip('\n')
                js = json.loads(sample)
                js["label"] = 0
                sample = json.dumps(js)
                if i in non_iot_index_training:
                    print(sample, file=file_training)
                elif i in non_iot_index_testing:
                    print(sample, file=file_testing)


# build_dataset()
build_corpus_neural_nets()
# enlarge_training_set()