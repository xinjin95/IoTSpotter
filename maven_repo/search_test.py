#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: search.py
@time: 6/27/21 10:40 PM
@desc:
"""
import requests

# url = 'https://search.maven.org/solrsearch/select?q=g:"com.google.inject"+AND+a:"guice"&core=gav&rows=20&wt=json'
# url = 'https://search.maven.org/solrsearch/select?q=g:"com.google.inject"&rows=20&wt=json'
# url = 'https://search.maven.org/solrsearch/select?q=a:"guice"&rows=20&wt=json'
# url = 'https://search.maven.org/remotecontent?filepath=com/jolira/guice/3.0.0/guice-3.0.0.pom'
url = 'https://search.maven.org/solrsearch/select?q=fc:"androidx.viewpager2.widget"&rows=20&wt=json'

resp = requests.get(url)

print(resp.content.decode("utf-8"))