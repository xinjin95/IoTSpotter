#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: preprocess.py
@time: 2/22/21 9:14 PM
@desc:
"""
import json
import langid
from text_processor import TextProcessor

path_training = "../../data/dataset/training_large.txt"
metadata_path = "../../data/androzoo/app_metadata.json"
save_path = "../../data/dataset/processed_english.json"

tp = TextProcessor("")
total_num = 0
with open(save_path, 'w+') as file_save:
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines()
            if lines is None or len(lines) == 0:
                break
            for i, line in enumerate(lines):
                try:
                    total_num += 1
                    print(total_num)
                    pkg_name, content = line.split(":", 1)
                    js = json.loads(content)
                    tp.text = js["description"]
                    language = langid.classify(tp.text)[0]
                    if language == 'en':
                        res = tp.process(remove_stop_word=True)
                        print(json.dumps({"pkg_name": pkg_name, "description": res}), file=file_save)
                except:
                    print(line)
