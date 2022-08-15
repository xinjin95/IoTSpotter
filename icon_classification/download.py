#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: download.py
@time: 5/3/21 9:50 AM
@desc:
"""
import json
import subprocess

# training_set_metadata_path = "../data/final_dataset/complete_dataset_metadata.txt"
training_set_metadata_path = "../data/androzoo/600_inspection/600_metadata_original.txt"
save_path = "data/test_data/"
# img_urls = []


def execute(cmd, cwd=save_path):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd=cwd)
    process.wait()


def download():
    with open(training_set_metadata_path, 'r') as file:
        for i, line in enumerate(file):
            js = json.loads(line)
            pkg_name = js["app_id"]
            print("{}-th {}".format(i, pkg_name))
            icon_url = js["icon"]
            cmd = "curl {} -o {}.png".format(icon_url, pkg_name)
            execute(cmd)


if __name__ == '__main__':
    download()