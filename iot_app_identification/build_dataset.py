#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: build_dataset.py
@time: 2/1/21 11:46 PM
@desc:
"""

import pandas as pd
from iot_app_identification.text_processor import TextProcessor
import json

df = pd.read_excel("../data/keyword/IoT-seed.xlsx", sheet_name="Integration")

pkg_names = df["app_id"]
descriptions = df["description"]
keywords = df["keywords"]

tp = TextProcessor("")
file = open("../data/keyword/IoT-seed.txt", 'a+')

for i, pkg_name in enumerate(pkg_names):
    description = descriptions[i]
    keyword = keywords[i]
    tp.text = description
    description_processed = tp.process(remove_stop_word=True)
    if "|" in keyword:
        words = keyword.split("|")
    else:
        words = keyword.split("\n")
    words_processed = []
    for word in words:
        word = word.strip().replace("\n", "")
        if word != "":
            words_processed.append(word)
    js = {"app_id": pkg_name, "description": description_processed, "keywords": words_processed}
    print(json.dumps(js), file=file)