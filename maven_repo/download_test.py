#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: download_test.py
@time: 6/28/21 10:42 AM
@desc:
"""
import requests
import shutil

url = 'https://search.maven.org/remotecontent?filepath=com/jolira/guice/3.0.0/guice-3.0.0.pom'
local_file_name = "data/test.pom"


def download(url, local_file_name):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_file_name, 'wb') as f:
            # shutil.copyfileobj(r.raw, f)
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


if __name__ == '__main__':
    download(url, local_file_name)