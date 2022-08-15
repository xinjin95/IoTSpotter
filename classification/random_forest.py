#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: random_forest.py
@time: 2/22/21 11:10 PM
@desc:
"""
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from classification.utility import load_data_set, load_data_set_by_label
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix

# path_training = "../data/dataset/training.txt"
# path_training = "../data/dataset/training_large.txt"
# path_test = "../data/dataset/test.txt"
# path_test = "../data/dataset/testing_large.txt"
path_training = "../data/final_dataset/dataset_traditional/training_set.txt"
path_validation = "../data/final_dataset/dataset_traditional/validation_set.txt"
path_test = "../data/final_dataset/dataset_traditional/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)
iot_texts, _ = load_data_set_by_label(path_training, 1)
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')
num_features = 4000
performance = []
feature_vector = []


def tune_parameters():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(iot_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]

    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']

    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)

    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]

    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]

    # Method of selecting samples for training each tree
    bootstrap = [True, False]

    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}

    clf = RandomForestClassifier(class_weight='balanced')
    logging_search = RandomizedSearchCV(estimator=clf, param_distributions= random_grid, n_iter = 100, cv = 5,
                                        verbose=2, random_state=42, n_jobs = -1)
    logging_search.fit(training_set, training_labels)
    print("\n\nInitial tuning on 3000 features", file=file_tuning)
    print("Tuned Random Forest Parameters: {}".format(logging_search.best_params_), file=file_tuning)
    print("Best score is {}".format(logging_search.best_score_), file=file_tuning)


def classify():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    validation_set = tfidf_converter.transform(validation_texts).toarray()
    clf = RandomForestClassifier(n_estimators=1200, max_features='sqrt', max_depth=120)
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    print("RandomForestClassifier:  max_depth=110", file=file_tuning)
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