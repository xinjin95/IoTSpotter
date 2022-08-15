#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: cnn.py
@time: 4/27/21 12:14 AM
@desc:
"""
# from classification.keras_utility import data_sample_load, model_load, glove_dictionary_load
from keras.preprocessing.text import Tokenizer

from utility import load_data_set, load_data_set_by_label
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Embedding, Bidirectional, Dense, LSTM, GlobalMaxPool1D, Dropout, RNN, BatchNormalization
from dictionary import Dictionary
import tensorflow as tf
# import json
# from keras.utils import plot_model
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix

path_training = "data/dataset_neural_net/training_set.txt"
path_validation = "data/dataset_neural_net/validation_set.txt"
path_test = "data/dataset_neural_net/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)

number_frequent_words = 3000
tokenizer = Tokenizer(num_words=number_frequent_words)
tokenizer.fit_on_texts(training_texts)

file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')


def evaluate_test(predict_labels):
    f1 = f1_score(test_labels, predict_labels)
    accuracy = accuracy_score(test_labels, predict_labels)
    precision = precision_score(test_labels, predict_labels)
    recall = recall_score(test_labels, predict_labels)
    print("F1: {}".format(f1), file=file_tuning)
    print("Accuracy: {}".format(accuracy), file=file_tuning)
    print("Precision: {}".format(precision), file=file_tuning)
    print("Recall: {}\n".format(recall), file=file_tuning)
    print("(tn, fp, fn, tp): {}\n".format(confusion_matrix(test_labels, predict_labels).ravel()), file=file_tuning)


def glove_dictionary_load(glove_dictionary_path=None):
    """
    load glove file to dictionary
    :param glove_dictionary_path: path to stanford glove file
    :return: dictionary of word embedding
    """
    if glove_dictionary_path is None:
        glove_dictionary_path = "/home/xxx/Documents/data/glove.6B/glove.6B.50d.txt"

    with open(glove_dictionary_path, encoding='utf-8') as file:
        content = file.readlines()
    glove = {}
    for line in content:
        line = line.split()
        word = line[0]
        vector = np.array([float(val) for val in line[1:]])
        glove[word] = vector
    return glove


def train_embedding():

    training_text_sequences = tokenizer.texts_to_sequences(training_texts)
    validation_text_sequences = tokenizer.texts_to_sequences(validation_texts)

    word_counts = Dictionary(tokenizer.word_counts)
    word_counts.dictionary = word_counts.sort_by_value()
    vocabulary = Dictionary(tokenizer.index_word).take_n_items(number_frequent_words)
    frequent_word_counts = word_counts.take_n_items(number_frequent_words)

    padding_length = -1  # final result is 5068
    for training_sample_sequence in training_text_sequences:
        if len(training_sample_sequence) > padding_length:
            padding_length = len(training_sample_sequence)
    training_sequences_padded = pad_sequences(training_text_sequences, maxlen=padding_length)
    validation_sequences_padded = pad_sequences(validation_text_sequences, maxlen=padding_length)

    embedding_dimension = 300  # depends on which glove dictionary file used
    glove_file = "/home/xxx/Documents/data/glove.6B/glove.6B.%dd.txt" % embedding_dimension
    glove_embedding = glove_dictionary_load(glove_dictionary_path=glove_file)
    embedding_matrix = np.zeros((number_frequent_words + 1, embedding_dimension))
    for index, word in vocabulary.items():
        if word is not None:
            word_vec = glove_embedding[word]
            if word_vec is not None:
                embedding_matrix[index] = word_vec

    # model architecture
    model = Sequential()
    embedding_layer = Embedding(number_frequent_words + 1, embedding_dimension, input_length=padding_length,
                                weights=[embedding_matrix])
    model.add(embedding_layer)
    # bidirectional_layer = Bidirectional(LSTM(50, return_sequences=True))
    convolutional_layer = keras.layers.Conv1D(filters=32, kernel_size=8, activation='relu')
    # model.add(bidirectional_layer)
    model.add(convolutional_layer)
    # model.add(BatchNormalization())
    pooling_layer = GlobalMaxPool1D()
    model.add(pooling_layer)
    model.add(Dense(60, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model_summary = model.summary()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    x_train, y_train = training_sequences_padded, training_labels
    x_validation, y_validation = validation_sequences_padded, validation_labels
    model.fit(x_train, y_train, epochs=20, batch_size=100, validation_data=(x_validation, y_validation))
    model.save("data/cnn_embedding_final.h5")


def classify_embedding():
    padding_length = 5068
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts+validation_texts)
    test_text_sequences = tokenizer.texts_to_sequences(test_texts)
    test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)

    model = keras.models.load_model("data/cnn_embedding_final.h5")
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted)


if __name__ == '__main__':
    # train_tfidf()
    # classify_tfidf()
    # try:
    #     with tf.device("/device:GPU:1"):
    #         train_embedding()
    # except RuntimeError as e:
    #     print(e)

    classify_embedding()