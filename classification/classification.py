#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: cnn.py
@time: 3/2/21 12:07 AM
@desc:
"""
from classification.keras_utility import data_sample_load, model_load, glove_dictionary_load
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from classification.utility import load_data_set, load_data_set_by_label
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Embedding, Bidirectional, Dense, LSTM, GlobalMaxPool1D, Dropout, RNN
from classification.dictionary import Dictionary
import json
from keras.utils import plot_model
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
from tensorflow.keras import backend as K


path_training = "../data/dataset/training_set.txt"
# path_training = "../data/final_dataset/dataset_neural_networks/training_set.txt"
path_validation = "../data/dataset/validation_set.txt"
# path_validation = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
path_test = "../data/dataset/test_set.txt"
# path_test = "../data/androzoo/600_inspection/600_metadata_with_label.txt"
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

    model = load_model("../data/classifiers/bilstm.h5")
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    print("Prediction:")
    print(labels_predicted)

if __name__ == '__main__':
    classification_test()