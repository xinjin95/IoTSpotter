#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: test_BiLSTM_on_600_apps.py
@time: 5/4/21 12:23 PM
@desc:
"""
import json
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix, classification_report

final_iot_path = "../data/androzoo/classification_result_iot_apps.txt"
test_app_metadata_path = "../data/androzoo/600_inspection/600_metadata_with_label.txt"

iot_apps = open(final_iot_path, 'r').read().strip().split('\n')
iot_apps = set(iot_apps)

labels_real = []
predictions = []


def get_labels():
    with open(test_app_metadata_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["app_id"]
            label_real = js["label"]
            label_real = int(label_real)

            if pkg_name in iot_apps:
                label_pred = 1
            else:
                label_pred = 0

            labels_real.append(label_real)
            predictions.append(label_pred)


def calculate_performane():
    test_labels = labels_real
    predict_labels = predictions
    f1 = f1_score(test_labels, predict_labels)
    accuracy = accuracy_score(test_labels, predict_labels)
    precision = precision_score(test_labels, predict_labels)
    recall = recall_score(test_labels, predict_labels)
    print("F1: {}".format(f1))
    print("Accuracy: {}".format(accuracy))
    print("Precision: {}".format(precision))
    print("Recall: {}\n".format(recall))
    print("(tn, fp, fn, tp): {}\n".format(confusion_matrix(test_labels, predict_labels).ravel()))
    print(classification_report(test_labels, predict_labels, target_names=["0", "1"]))

if __name__ == '__main__':
    get_labels()
    calculate_performane()