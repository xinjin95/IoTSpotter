#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: analyze_result.py
@time: 8/10/21 12:14 PM
@desc:
"""
import json
import glob
import xmltodict

result_dir = "data/analysis_results/"


def get_target_package_names():
    pass


def process_one_result(path_to_file):
    with open(path_to_file, 'r') as f:
        for line in f:
            # line = line.strip('\n')
            try:
                js = xmltodict.parse(line)
                print(json.dumps(js))

            except:
                print(path_to_file)


def main():
    files = glob.glob(result_dir + '*')
    for file in files:
        if not file.endswith('.xml'):
            continue
        process_one_result(file)


if __name__ == '__main__':
    main()