#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: large_scale_classify.py
@time: 3/28/21 10:51 AM
@desc:
"""
import json

original_metadata_path = "../data/androzoo/app_metadata.json"
englist_processed_path = "../data/dataset/processed_english.json"
new_metadata_path = "../data/dataset/english_metadata.json"

def get_english_pkgs():
    pkgs = []
    with open(englist_processed_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                js = json.loads(line)
                pkgs.append(js["pkg_name"])
    return set(pkgs)


def collect_english_metadata():
    english_pkgs = get_english_pkgs()
    print("Get {} english apps".format(len(english_pkgs)))
    total = 0
    new_metadata_file = open(new_metadata_path, 'a+')
    with open(original_metadata_path, 'r') as file:
        while True:
            lines = file.readlines()
            if lines is None or len(lines) == 0:
                break
            for line in lines:
                try:
                    pkg_name, content = line.split(":", 1)
                    if pkg_name not in english_pkgs:
                        continue
                    # print(line)
                    js = json.loads(content)
                    description = js["description"]
                    title = js["title"]
                    print(json.dumps({"pkg_name": pkg_name, "title": title, "description": description}), file=new_metadata_file)
                    total += 1
                    print(total)
                except:
                    print(line)



if __name__ == '__main__':
    collect_english_metadata()