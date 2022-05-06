#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: get_old_package_names.py
@time: 7/12/21 2:06 PM
@desc:
"""
import os

old_2019_path = "../data/old_app_in_server/2019_01.txt"
old_2020_path = "../data/old_app_in_server/2020_06.txt"

save_2020_path = "../data/old_app_in_server/2020_06_pkgs.txt"
save_2019_path = "../data/old_app_in_server/2019_01_pkgs.txt"

# os.path.basename("/storage3/apks/2020.06/com.facebook.lite.apk")


def process(src_path, des_path):
    save_file = open(des_path, 'a+')
    with open(src_path, 'r') as src:
        for i, line in enumerate(src):
            print(i, "-th line")
            line = line.strip('\n')
            base_name = os.path.basename(line)
            if base_name.endswith('.apk'):
                # print(base_name, base_name[:-4])
                base_name = base_name[:-4]
                print(base_name, file=save_file)


if __name__ == '__main__':
    process(old_2020_path, save_2020_path)