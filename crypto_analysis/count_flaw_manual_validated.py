#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: count_flaw_manual_validated.py
@time: 2/1/22 1:38 PM
@desc:
"""

from collections import Counter

lines = open("data/crypto_validation.txt", 'r').read().strip().split('\n')
counter = Counter(lines)
print(counter.most_common())