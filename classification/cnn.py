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

small_training = "../data/dataset/neural_nets_corpus/training_small_set.txt"
small_validation = "../data/dataset/neural_nets_corpus/validation_small_set.txt"

large_training = "../data/dataset/neural_nets_corpus/training_large_set.txt"
large_validation = "../data/dataset/neural_nets_corpus/validation_large_set.txt"

# test_set_path = "../data/dataset/neural_nets_corpus/test_set.txt"
# test_set_path = "../data/androzoo/600_inspection/600_metadata_with_label.txt"

amazon_set_path = "../data/dataset/amazon/description_set.txt"

# train_set_path = small_training
# validation_set_path = small_validation
path_training = "../data/final_dataset/dataset_neural_networks/training_set_backup.txt"
# path_training = "../data/final_dataset/dataset_neural_networks/training_set.txt"
path_validation = "../data/final_dataset/dataset_neural_networks/validation_set_backup.txt"
# path_validation = "../data/final_dataset/dataset_neural_networks/validation_set.txt"
path_test = "../data/final_dataset/dataset_neural_networks/test_set.txt"
# path_test = "../data/androzoo/600_inspection/600_metadata_with_label.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)
iot_texts, _ = load_data_set_by_label(path_training, 1)
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')

num_features = 3000
tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
tfidf_converter.fit(iot_texts)

number_frequent_words = 3000
tokenizer = Tokenizer(num_words=number_frequent_words)
tokenizer.fit_on_texts(training_texts)

# test_texts, test_labels = load_data_set("")


def train_tfidf():
    # tf_len = len(tfidf_converter.vocabulary_)
    training_set = tfidf_converter.transform(training_texts).toarray()
    training_set = training_set.reshape(training_set.shape[0], training_set.shape[1], 1)
    validation_set = tfidf_converter.transform(validation_texts).toarray()
    validation_set = validation_set.reshape(validation_set.shape[0], validation_set.shape[1], 1)
    model = Sequential()
    # model.add(keras.layers.Input(batch_shape=(None, tf_len, 1)))
    model.add(keras.layers.Conv1D(filters=32, kernel_size=5, activation='relu'))
    model.add(keras.layers.Dropout(0.81))
    pooling_layer = keras.layers.MaxPooling1D(pool_size=2)

    model.add(pooling_layer)
    model.add(keras.layers.Flatten())
    # model.add(keras.layers.Dense(1000, kernel_initializer=keras.initializers.he_normal(seed=1), activation='tanh',
    #                              input_dim=3000))
    # model.add(keras.layers.Dropout(0.81))
    model.add(keras.layers.Dense(500, kernel_initializer=keras.initializers.he_normal(seed=2), activation='relu'))
    model.add(keras.layers.Dropout(0.81))
    model.add(Dense(60, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(training_set, training_labels, epochs=20, batch_size=512, validation_data=(validation_set,
                                                                                         validation_labels))
    model_summary = model.summary()
    model.save(filepath="../data/classifiers/cnn.h5")


def classify_tfidf():
    test_set = tfidf_converter.transform(test_texts).toarray()
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1], 1)
    model = load_model("../data/classifiers/cnn.h5")
    prediction = model.predict(test_set)
    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted)


def evaluate_test(predict_labels, msg=None):
    f1 = f1_score(test_labels, predict_labels)
    accuracy = accuracy_score(test_labels, predict_labels)
    precision = precision_score(test_labels, predict_labels)
    recall = recall_score(test_labels, predict_labels)
    if msg is not None:
        print(msg, file=file_tuning)
    print("F1: {}".format(f1), file=file_tuning)
    print("Accuracy: {}".format(accuracy), file=file_tuning)
    print("Precision: {}".format(precision), file=file_tuning)
    print("Recall: {}\n".format(recall), file=file_tuning)
    print(classification_report(test_labels, predict_labels), file=file_tuning)

    if msg is not None:
        print(msg, file=file_tuning)
    print("F1: {}".format(f1))
    print("Accuracy: {}".format(accuracy))
    print("Precision: {}".format(precision))
    print("Recall: {}\n".format(recall))
    print(classification_report(test_labels, predict_labels))
    # performance.append([f1, accuracy, precision, recall])


def train_embedding():

    training_text_sequences = tokenizer.texts_to_sequences(training_texts)
    validation_text_sequences = tokenizer.texts_to_sequences(validation_texts)

    word_counts = Dictionary(tokenizer.word_counts)
    word_counts.dictionary = word_counts.sort_by_value()
    vocabulary = Dictionary(tokenizer.index_word).take_n_items(number_frequent_words)
    frequent_word_counts = word_counts.take_n_items(number_frequent_words)

    padding_length = -1  # final result is 494
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
    pooling_layer = GlobalMaxPool1D()
    model.add(pooling_layer)
    model.add(Dense(60, activation='tanh'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model_summary = model.summary()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    x_train, y_train = training_sequences_padded, training_labels
    x_validation, y_validation = validation_sequences_padded, validation_labels
    # model.fit(x_train, y_train, epochs=20, batch_size=512, validation_data=(x_validation, y_validation))
    model.fit(x_train, y_train, epochs=100, batch_size=100, validation_data=(x_validation, y_validation))
    model.save("../data/classifiers/cnn_embedding_backup.h5")

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

def classify_embedding():

    padding_length = 493
    number_frequent_words = 3000
    tokenizer = Tokenizer(num_words=number_frequent_words)
    tokenizer.fit_on_texts(training_texts+validation_texts)
    test_text_sequences = tokenizer.texts_to_sequences(test_texts)
    test_sequences_padded = pad_sequences(test_text_sequences, maxlen=padding_length)

    model = model_load("../data/classifiers/cnn_embedding_backup.h5")
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted, "bilstm_embedding_final_precision")


def classification_test():
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

    # model = model_load("../data/classifiers/bilstm_embedding_final_precision.h5")
    # model = load_model("../data/classifiers/bilstm_embedding_new_data_included_double_no_pooling.h5", custom_objects=dependencies)
    model = load_model("../data/classifiers/cnn_embedding_final.h5")
    x_test = test_sequences_padded
    prediction = model.predict(x_test)

    labels_predicted = [int(value > 0.5) for value in prediction]
    evaluate_test(labels_predicted, "cnn")

if __name__ == '__main__':
    # train_tfidf()
    # classify_tfidf()
    # train_embedding()
    # classify_embedding()
    classification_test()