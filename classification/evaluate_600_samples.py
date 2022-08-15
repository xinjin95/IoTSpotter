#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: evaluate_600_samples.py
@time: 4/6/21 11:33 AM
@desc:
"""

import json
from keras.preprocessing.text import Tokenizer
from classification.utility import load_data_set
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from classification.keras_utility import data_sample_load, model_load
from keras.models import load_model

samples_path = "../data/androzoo/600_inspection/600_metadata_with_label.txt"
path_training = "../data/final_dataset/dataset_neural_networks/training_set.txt"
path_validation = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def load_samples():
    descriptions = []
    app_ids = []
    labels = []
    sources = []
    with open(samples_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            app_ids.append(js["app_id"])
            descriptions.append(js["description"])
            labels.append(js["label"])
            sources.append(js["source"])
    return app_ids, descriptions, labels, sources


test_ids, test_texts, test_labels, test_sources = load_samples()
# print(test_labels)


def evaluate_test(predict_labels):
    f1 = f1_score(test_labels, predict_labels)
    accuracy = accuracy_score(test_labels, predict_labels)
    precision = precision_score(test_labels, predict_labels)
    recall = recall_score(test_labels, predict_labels)
    print("F1: {}".format(f1), file=file_tuning)
    print("Accuracy: {}".format(accuracy), file=file_tuning)
    print("Precision: {}".format(precision), file=file_tuning)
    print("Recall: {}\n".format(recall), file=file_tuning)


def classify():
    padding_length = 493
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts + validation_texts)
    test_text_sequences = tokenizer.texts_to_sequences(test_texts)
    test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)

    dependencies = {
        'f1_m': f1_m,
        'recall_m': recall_m,
        'precision_m': precision_m
    }

    model = load_model("../data/classifiers/bilstm_embedding_final_precision.h5", custom_objects=dependencies)
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted)


if __name__ == '__main__':
    classify()