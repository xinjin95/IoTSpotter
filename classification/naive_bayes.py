#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: naive_bayes.py
@time: 2/22/21 9:59 PM
@desc:
"""
from classification.utility import load_data_set, load_data_set_by_label
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt
import json
import random

# path_training = "../data/dataset/training.txt"
# path_training = "../data/dataset/training_large.txt"
# path_test = "../data/dataset/test.txt"
# path_test = "../data/dataset/testing_large.txt"
path_training = "../data/final_dataset/dataset_traditional/training_set.txt"
path_validation = "../data/final_dataset/dataset_traditional/validation_set.txt"
path_test = "../data/final_dataset/dataset_traditional/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
test_texts, test_labels = load_data_set(path_test)
validation_texts, validation_labels = load_data_set(path_validation)
iot_texts, _ = load_data_set_by_label(path_training, 1)
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')
num_features = 3000
performance = []
feature_vector = []


def classify():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    validation_set = tfidf_converter.transform(validation_texts).toarray()
    clf = naive_bayes.GaussianNB()
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    print("CategoricalNB:", file=file_tuning)
    evaluate_test(prediction, use_validation=False)


def evaluate_test(predict_labels, use_validation=True):
    if use_validation:
        real_labels = validation_labels
    else:
        real_labels = test_labels
    f1 = f1_score(real_labels, predict_labels)
    accuracy = accuracy_score(real_labels, predict_labels)
    precision = precision_score(real_labels, predict_labels)
    recall = recall_score(real_labels, predict_labels)
    print("F1: {}".format(f1), file=file_tuning)
    print("Accuracy: {}".format(accuracy), file=file_tuning)
    print("Precision: {}".format(precision), file=file_tuning)
    print("Recall: {}\n".format(recall), file=file_tuning)
    performance.append([f1, accuracy, precision, recall])


if __name__ == '__main__':
    classify()