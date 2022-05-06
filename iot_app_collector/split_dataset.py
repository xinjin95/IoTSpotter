#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: split_dataset.py
@time: 3/1/21 11:41 PM
@desc:
"""
import random
import json

small_dataset = "../data/dataset/neural_nets_corpus/training_validation_small_set.txt"
large_dataset = "../data/dataset/neural_nets_corpus/training_validation_large_set.txt"

small_training = "../data/dataset/neural_nets_corpus/training_small_set.txt"
small_validation = "../data/dataset/neural_nets_corpus/validation_small_set.txt"

large_training = "../data/dataset/neural_nets_corpus/training_large_set.txt"
large_validation = "../data/dataset/neural_nets_corpus/validation_large_set.txt"


def split_dataset(file_src, file_training, file_validation):
    lines = open(file_src, 'r').read().strip().split('\n')
    # dids = set()
    # training_lines = random.sample(lines, int(0.8*len(lines)))
    with open(file_training, 'w+') as training:
        with open(file_validation, 'w+') as validation:
            for line in lines:
                line = line.strip().strip('\n')
                random_val = random.random()
                if random_val >= 0.8:
                    print(line, file=validation)
                else:
                    print(line, file=training)


def check_duplication(file_path):
    dids = set()
    with open(file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js['pkg_name']
            if pkg_name in dids:
                print(pkg_name)
            dids.add(pkg_name)


if __name__ == '__main__':
    # check_duplication(large_dataset)
    split_dataset(small_dataset, small_training, small_validation)
    split_dataset(large_dataset, large_training, large_validation)