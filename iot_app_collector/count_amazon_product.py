#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: count_amazon_product.py
@time: 10/19/21 8:44 PM
@desc:
"""
import json

with open("../data/amazon/description_.json", 'r') as f:
    js = json.load(f)


    # print(len(js))