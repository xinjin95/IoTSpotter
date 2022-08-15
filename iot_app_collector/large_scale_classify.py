#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: large_scale_classify.py
@time: 3/28/21 11:26 AM
@desc:
"""
from keras.models import load_model
# from iot_app_collector.text_processor import TextProcessor
import json
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


path_training = "../data/dataset/training_set.txt"
path_validation = "../data/dataset/validation_set.txt"


def load_data_set(path_file):
    texts = []
    labels = []
    with open(path_file, 'r') as file:
        for line in file:
            line = line.strip("\n")
            js = json.loads(line)
            texts.append(js["description"])
            labels.append(js["label"])
    labels = np.asarray(labels, dtype=np.int)
    return texts, labels


def main():
    training_texts, training_labels = load_data_set(path_training)
    validation_texts, validation_labels = load_data_set(path_validation)

    new_metadata_path = "../data/dataset/english_metadata.json"
    bilistm_model_path = "../data/dataset/bilstm_embedding_final_generator.h5"

    # tp = TextProcessor("")
    padding_length = 493
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)

    tokenizer.fit_on_texts(training_texts + validation_texts)
    model = load_model(bilistm_model_path)
    # result = model.predict_generator(generator=)
    file_save = open("../data/dataset/classification_result.csv", 'a+')
    total = 0
    with open(new_metadata_path, 'r') as file:
        while True:
            # while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            test_texts = []
            pkgs = []
            for line in lines:
                js = json.loads(line)
                description = js["description"]
                title = js["title"]
                pkg = js["pkg_name"]
                pkgs.append(pkg)
                text = title + " " + description
                # text = tp.process(stem_words=False)
                test_texts.append(text)
            test_text_sequences = tokenizer.texts_to_sequences(test_texts)
            test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)
            x_test = test_sequences_padded
            prediction = model.predict(x_test)

            labels_predicted = [int(value > 0.5) for value in prediction]
            for i, label in enumerate(labels_predicted):
                print("{},{}".format(pkgs[i], label), file=file_save)
                total += 1
                print(total)


if __name__ == '__main__':
    main()