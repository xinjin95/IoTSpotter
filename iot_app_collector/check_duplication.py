#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: check_duplication.py
@time: 2/22/21 9:46 AM
@desc:
"""
import json

metadata_path = "../data/androzoo/app_metadata.json"
app_id_mismatch = "../data/androzoo/id_mismatch.txt"
app_duplication = "../data/androzoo/id_duplication.txt"

print("finished list reading")
dids = set()
total = 0
file_duplication = open(app_duplication, 'a+')
file_mismatch = open(app_id_mismatch, 'a+')
with open(metadata_path, 'r') as file:
    while True:
        lines = file.readlines()
        if lines is None or len(lines) == 0:
            break
        for line in lines:
            try:
                pkg_name, content = line.split(":", 1)
                js = json.loads(content)
                app_id = js['app_id']
                if app_id != pkg_name:
                    print(pkg_name, file=file_mismatch)
                if pkg_name in dids:
                    print(pkg_name, file=file_duplication)
                dids.add(pkg_name)
                total += 1
                print(total)
            except:
                print(line)