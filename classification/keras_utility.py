#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: keras_utility.py
@time: 3/26/20 10:46 AM
@description: this file has some common methods used in training and inference for keras
"""

import numpy as np
from iot_app_collector.text_processor import TextProcessor
import json
from keras.models import load_model
from keras.utils import plot_model


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


def data_sample_process(data_sample_path, remove_stop_words=True, stem_words=True, use_model_filter=False):
    """
    process text and label from data sample if a path to target data set file is given
    :param use_model_filter: use glove dictionary to filter the texts
    :param stem_words: if True, stem words in text samples
    :param remove_stop_words: if True, remove stop words from text samples
    :param data_sample_path: path to target data set file
    :return: list of texts and labels
    """
    texts = []
    labels = []
    processor = TextProcessor(text="")
    glove_model = None
    if use_model_filter:
        glove_model = glove_dictionary_load()
    with open(data_sample_path, 'r') as file:
        for line in file:
            if line.endswith('\n'):
                line = line.replace('\n', '')
            js = json.loads(line)
            text = js["text"]
            label = js["label"]
            labels.append(label)
            if isinstance(text, list):
                text_result = ""
                for text_element in text:
                    processor.text = text_element
                    text_element = processor.process(remove_stop_word=remove_stop_words, stem_words=False,
                                                     use_model_filter=use_model_filter, model_embedding=glove_model)
                    text_result += ' ' + text_element
                texts.append(text_result)
            else:
                processor.text = text
                text = processor.process(remove_stop_word=remove_stop_words, stem_words=False)
                texts.append(text)
    return texts, labels


def data_sample_load(data_set_path, is_label_binary):
    """
    load data sample from file
    :param is_label_binary: if True, the label in labels will be binary, otherwise label is positive int number
    :param data_set_path: the path of target data set file
    :return: texts is list of text samples, labels is list of corresponding sample
    """
    texts = []
    labels = []
    with open(data_set_path, 'r') as file:
        for line in file:
            if line.endswith('\n'):
                line = line.replace('\n', '')
            js = json.loads(line)
            text = js["description"]
            label = js["label"]
            labels.append(label)
            texts.append(text)
    labels = label_vectorization(labels, is_label_binary)
    return texts, labels


def label_vectorization(labels, is_label_binary):
    """
    create vectors of labels, like [0,1,0] -> [1,2,3] -> [[1,0,0],[0,1,0],[0,0,1]]

    :param is_label_binary: if True,
    the label in labels will be binary, otherwise label is positive int number

    :param labels: list of numeric
    numbers, it must be continuous numbers and starts at 1 if is_label_binary is False; otherwise, label in labels
    will be 0 or 1 :return: 2-D matrix
    """
    if is_label_binary:
        return labels
    else:
        result = np.zeros((len(labels), max(labels)))
        for i, label in enumerate(labels):
            result[i][label - 1] = 1
    return result


def model_load(path_to_model):
    """
    load model from h5 model file
    :param path_to_model: the path to target model
    :return: model including architecture and parameters
    """
    return load_model(path_to_model)


def model_visualization(model, image_save_path):
    """
    plot model and save to image file
    :param model: model built or load from model_load() method
    :param image_save_path: path to save the image of model
    :return: null
    """
    plot_model(model, image_save_path)


if __name__ == "__main__":
    # tp = TextProcessor("")
    # tp.text = "0   18 out in  116  12  14 aliiiii youve"
    # glove = glove_dictionary_load()
    # res = tp.process(remove_stop_word=False, model_embedding=glove, use_model_filter=True)
    # print(res)
    # layout_model = model_load("../data/classifier/input_classifier_keras.h5")
    # layout_model.summary()
    # model_visualization(layout_model, "../data/classifier/image_input_model.png")
    model_path = "../data/classifiers/cnn.h5"
    model = model_load(model_path)
    model_fig_path = "../data/classifiers/cnn.png"
    model_visualization(model, model_fig_path)

