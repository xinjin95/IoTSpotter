#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_sunil_new_pkgs.py
@time: 5/11/21 12:27 AM
@desc:
"""
sunil_new = "../data/androzoo/description-improvement/after_sunil_labeling_58K.txt"
save_path = "../data/androzoo/description-improvement/after_sunil_labeling_58K_pkgs.txt"

with open(save_path, 'w+') as des:
    with open(sunil_new, 'r') as src:
        for line in src:
            pkg_name, content = line.split('\t', 1)
            pkg_name = pkg_name.strip()
            print(pkg_name, file=des)