#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: package_name_line_parse_test.py
@time: 6/29/21 1:04 PM
@desc:
"""

result_file_path = "data/search_result.txt"
good_line = 0
bad_line = 0

with open(result_file_path, 'r') as file:
    while True:
        lines = file.readlines(2000)
        if lines is None or len(lines) == 0:
            break
        # for line in lines:
        #     pkg_queue.append(line)
        # total += len(pkg_queue)
        # while len(pkg_queue) > 0:
        for line in lines:
            try:
                pkg_name, content = line.split(':', 1)
                good_line += 1
            except:
                print(line)
                bad_line += 1
    print(good_line)
    print(bad_line)