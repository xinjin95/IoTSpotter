#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""
from itertools import islice


class Dictionary(object):

    def __init__(self, dictionary):
        """
        process dictionary
        :param dictionary: target dictionary
        """
        self.dictionary = dictionary

    def sort_by_value(self, decreasing_order=True):
        """
        sort dictionary by value
        :param decreasing_order: if True, sort it with decreasing order
        :return: processed dictionary
        """
        return {k: v for k, v in sorted(self.dictionary.items(), key=lambda item: item[1], reverse=decreasing_order)}

    def sort_by_key(self, decreasing_order=True):
        return {k: v for k, v in sorted(self.dictionary.items(), key=lambda item: item[0], reverse=decreasing_order)}

    def take_n_items(self, n):
        """
        take n items from target dictionary
        :param n: number of items to take
        :return: a processed dictionary
        """
        return dict(islice(self.dictionary.items(), n))


if __name__ == "__main__":
    # cars = {"a": 1, "b": 5, "c": 2, "d": 10}
    num = {3: 0, 1: 2, 5: 3}
    dic = Dictionary(num)
    #dic.dictionary = dic.sort_by_value()
    # res = dic.take_n_items(2)
    res = dic.sort_by_key()
    print(res)
