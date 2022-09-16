#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import json
import numpy as np


path_training = "../data/dataset/training_set.txt"
path_validation = "../data/dataset/validation_set.txt"
path_test = "../data/dataset/test_set.txt"
path_model = "../data/classifiers/bilstm.h5"

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

training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)

def classification_test():
    padding_length = 493
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts + validation_texts)
    test_text_sequences = tokenizer.texts_to_sequences(test_texts)
    test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)

    model = load_model(path_model)
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    print("Prediction:")
    print(labels_predicted)

if __name__ == '__main__':
    classification_test()