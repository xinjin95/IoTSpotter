#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: rnn.py
@time: 3/2/21 1:50 AM
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
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from cnn import evaluate_test

small_training = "../data/dataset/neural_nets_corpus/training_small_set.txt"
small_validation = "../data/dataset/neural_nets_corpus/validation_small_set.txt"

large_training = "../data/dataset/neural_nets_corpus/training_large_set.txt"
large_validation = "../data/dataset/neural_nets_corpus/validation_large_set.txt"

test_set_path = "../data/dataset/neural_nets_corpus/test_set.txt"

# path_training = "../data/final_dataset/dataset_neural_networks/training_set.txt"
path_training = "../data/final_dataset/dataset_neural_networks/training_set_backup.txt"
# path_validation = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
path_validation = "../data/final_dataset/dataset_neural_networks/validation_set_backup.txt"
path_test = "../data/final_dataset/dataset_neural_networks/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)
iot_texts, _ = load_data_set_by_label(path_training, 1)
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')

# num_features = 3000
# tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
# tfidf_converter.fit(training_texts)


def train_embedding():
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts)
    training_text_sequences = tokenizer.texts_to_sequences(training_texts)
    validation_text_sequences = tokenizer.texts_to_sequences(validation_texts)

    word_counts = Dictionary(tokenizer.word_counts)
    word_counts.dictionary = word_counts.sort_by_value()
    vocabulary = Dictionary(tokenizer.index_word).take_n_items(number_frequent_words)
    frequent_word_counts = word_counts.take_n_items(number_frequent_words)

    padding_length = -1  # final result is 560
    for training_sample_sequence in training_text_sequences:
        if len(training_sample_sequence) > padding_length:
            padding_length = len(training_sample_sequence)
    training_sequences_padded = pad_sequences(training_text_sequences, maxlen=padding_length)
    validation_sequences_padded = pad_sequences(validation_text_sequences, maxlen=padding_length)

    embedding_dimension = 300  # depends on which glove dictionary file used
    glove_file = "/home/xin/Documents/data/glove.6B/glove.6B.%dd.txt" % embedding_dimension
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
    # bidirectional_layer = Bidirectional(LSTM(50, return_sequences=True))
    bidirectional_layer = keras.layers.SimpleRNN(units=300, return_sequences=True)
    model.add(bidirectional_layer)
    pooling_layer = GlobalMaxPool1D()
    model.add(pooling_layer)
    model.add(Dense(60, activation='tanh'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model_summary = model.summary()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # model training
    x_train, y_train = training_sequences_padded, training_labels
    x_validation, y_validation = validation_sequences_padded, validation_labels
    model.fit(x_train, y_train, epochs=20, batch_size=512, validation_data=(x_validation, y_validation))

    model.save("../data/classifiers/rnn_embedding_final.h5")


def classify_embedding():

    padding_length = 493
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts+validation_texts)
    test_text_sequences = tokenizer.texts_to_sequences(test_texts)
    test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)

    model = model_load("../data/classifiers/rnn_embedding.h5")
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted, "bilstm_embedding_final_precision")

if __name__ == '__main__':
    # train_embedding()
    classify_embedding()