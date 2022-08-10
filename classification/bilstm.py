#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: bilstm.py
@time: 3/2/21 2:28 AM
@desc:
"""
# from classification.keras_utility import data_sample_load, model_load, glove_dictionary_load
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from classification.utility import load_data_set, load_data_set_by_label
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
# import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, Bidirectional, Dense, LSTM, GlobalMaxPool1D, Dropout, RNN, BatchNormalization
# from classification.dictionary import Dictionary
from dictionary import Dictionary
from tensorflow.keras.utils import Sequence
import math
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.metrics import *
from tensorflow.keras import backend as K

import json
# from keras.utils import plot_model
# from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

# small_training = "../data/dataset/neural_nets_corpus/training_small_set.txt"
# small_validation = "../data/dataset/neural_nets_corpus/validation_small_set.txt"
#
# large_training = "../data/dataset/neural_nets_corpus/training_large_set.txt"
# large_validation = "../data/dataset/neural_nets_corpus/validation_large_set.txt"

# test_set_path = "../data/dataset/neural_nets_corpus/test_set.txt"

# path_training = "../data/final_dataset/dataset_neural_networks/training_set.txt"
# path_validation = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
path_training = "../data/dataset/training_set.txt"
path_validation = "../data/dataset/validation_set.txt"
# path_test = "../data/final_dataset/dataset_neural_networks/test_set.txt"

# test_texts, test_labels = load_data_set(path_test)
# iot_texts, _ = load_data_set_by_label(path_training, 1)
# file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')

# num_features = 3000
# tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
# tfidf_converter.fit(iot_texts)


def glove_dictionary_load(glove_dictionary_path=None):
    """
    load glove file to dictionary
    :param glove_dictionary_path: path to stanford glove file
    :return: dictionary of word embedding
    """
    if glove_dictionary_path is None:
        # glove_dictionary_path = "/home/xin/Documents/data/glove.6B/glove.6B.50d.txt"
        glove_dictionary_path = "../data/glove/glove.6B.300d.txt"

    with open(glove_dictionary_path, encoding='utf-8') as file:
        content = file.readlines()
    glove = {}
    for line in content:
        line = line.split()
        word = line[0]
        vector = np.array([float(val) for val in line[1:]])
        glove[word] = vector
    return glove


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


class DataGenerator(Sequence):
    def __init__(self, x_set, y_set, batch_size):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size

    def __len__(self):
        return math.ceil(len(self.y) / self.batch_size)

    def __getitem__(self, idx):
        # print("working on {}".format(idx))
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]
        return batch_x, batch_y


def train_embedding():
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts+validation_texts)
    training_text_sequences = tokenizer.texts_to_sequences(training_texts)
    validation_text_sequences = tokenizer.texts_to_sequences(validation_texts)

    word_counts = Dictionary(tokenizer.word_counts)
    word_counts.dictionary = word_counts.sort_by_value()
    vocabulary = Dictionary(tokenizer.index_word).take_n_items(number_frequent_words)
    frequent_word_counts = word_counts.take_n_items(number_frequent_words)

    padding_length = -1  # final result is 493
    for training_sample_sequence in training_text_sequences:
        if len(training_sample_sequence) > padding_length:
            padding_length = len(training_sample_sequence)
    training_sequences_padded = pad_sequences(training_text_sequences, maxlen=padding_length)
    validation_sequences_padded = pad_sequences(validation_text_sequences, maxlen=padding_length)

    embedding_dimension = 300  # depends on which glove dictionary file used
    # glove_file = "/home/xin/Documents/data/glove.6B/glove.6B.%dd.txt" % embedding_dimension
    glove_file = "../data/glove/glove.6B.%dd.txt" % embedding_dimension
    glove_embedding = glove_dictionary_load(glove_dictionary_path=glove_file)
    embedding_matrix = np.zeros((number_frequent_words + 1, embedding_dimension))
    for index, word in vocabulary.items():
        if word is not None:
            word_vec = glove_embedding[word]
            if word_vec is not None:
                embedding_matrix[index] = word_vec

    model = Sequential()
    embedding_layer = Embedding(number_frequent_words + 1, embedding_dimension, input_length=padding_length,
                                weights=[embedding_matrix])
    model.add(embedding_layer)
    bidirectional_layer = Bidirectional(LSTM(units=300, return_sequences=True))
    # bidirectional_layer = LSTM(50, return_sequences=True)
    model.add(bidirectional_layer)
    # model.add(Bidirectional(LSTM(units=300, return_sequences=True)))
    pooling_layer = GlobalMaxPool1D()
    model.add(pooling_layer)
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    # model.add(Dense(100, activation='tanh'))
    # output_dimensions = len(training_labels[0])
    # model.add(Dense(1, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model_summary = model.summary()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # model training
    x_train, y_train = training_sequences_padded, training_labels
    x_validation, y_validation = validation_sequences_padded, validation_labels
    model.fit(x_train, y_train, epochs=100, batch_size=100, validation_data=(x_validation, y_validation))
    # training_generator = DataGenerator(x_set=x_train, y_set=y_train, batch_size=100)
    # validation_generator = DataGenerator(x_set=x_validation, y_set=y_validation, batch_size=100)
    model_save_path = "../data/classifiers/bilstm_new_training.h5"
    # checkpoint = ModelCheckpoint(model_save_path, monitor='val_accuracy', verbose=0, save_best_only=True,
    #                              save_weights_only=False, mode='auto')
    # model.fit_generator(training_generator, steps_per_epoch=math.ceil(len(y_train)/100), epochs=100, verbose=1,
    #                     validation_data=validation_generator, validation_steps=math.ceil(len(y_validation)/100),
    #                     callbacks=[checkpoint])
    # model.fit()

    model.save(model_save_path)


if __name__ == '__main__':
    tf.debugging.set_log_device_placement(False)
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        train_embedding()
