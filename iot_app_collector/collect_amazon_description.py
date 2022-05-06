#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_amazon_description.py
@time: 3/2/21 1:55 AM
@desc:
"""
# import json
from iot_app_collector.text_processor import TextProcessor, glove_dictionary_load
import json

path_description = "../data/amazon/description_.json"
path_dataset = "../data/dataset/amazon/description_set.txt"

with open(path_description, 'r') as file:
    tp = TextProcessor("")
    glove_model = glove_dictionary_load()
    data = json.load(file)
    with open(path_dataset, 'w+') as file_save:
        for product in data:
            product_name = product['product_name']
            description = product['top_description'] + " " + product['bottom_description']
            tp.text = description
            description_processed = tp.process(stem_words=False, use_model_filter=True, model_embedding=glove_model)
            sample = json.dumps({"product_name": product_name, "description": description_processed, "label": 1})
            print(sample, file=file_save)


