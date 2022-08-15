#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: rank_iot_apps_by_installs.py
@time: 9/8/21 6:10 PM
@desc:
"""
import json
from classification.dictionary import Dictionary
import pandas as pd

metadata_path = '../data/androzoo/description-improvement/new_shared_37K_metadata.txt'


def get_app_installs():
    res = dict()
    with open(metadata_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js['app_id']
            installs = js['installs']
            tmp = installs.replace(',', '').replace('+', '')
            tmp = int(tmp)
            res[app_name] = tmp

    dictionary = Dictionary(res)
    res = dictionary.sort_by_value()
    return res


def main():
    res = get_app_installs()
    df = pd.DataFrame({"app_name": list(res.keys()), 'install_num': list(res.values())})
    df.to_csv("../data/androzoo/description-improvement/shared_37K_pkg_download_rank.csv", index=False)


if __name__ == '__main__':
    main()