#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collection_parse_failure_reason.py
@time: 4/19/21 11:24 AM
@desc:
"""

parse_log_path = "data/parse_log.txt"

reason = {}

with open(parse_log_path, 'r') as file:
    for line in file:
        res = line.split(',')
        res = res[2]
        if "failed - " in res:
            res = res.replace("failed - ", '')
            if res not in reason.keys():
                reason[res] = 0
            reason[res] += 1

print(reason)