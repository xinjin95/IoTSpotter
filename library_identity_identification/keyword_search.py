#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: keyword_search.py
@time: 6/21/21 10:11 AM
@desc:
"""
import time

import github.GithubException
from github import Github
import pandas as pd
import json
import argparse
import traceback

token_dict = {0: "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",
              1: "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",
              2: "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",
              3: "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" }

user_dict = {0: "xxxxxx95", 1: "autosign01", 2: "autosign02", 3: "autosign03"}
#
lib_freq_path = "../third_party_library/data/lib_frequency.csv"


def get_finished_packages(index):
    finished = set()
    save_path = "data/github_search_result/{}.txt".format(index)
    with open(save_path, 'r') as src:
        for line in src:
            js = json.loads(line)
            for key in js.keys():
                finished.add(key)
    return finished


def search(g, keyword, top_n):
    repositories = g.search_repositories(query=keyword)
    print("{}: search result list: {}".format(keyword, repositories.totalCount))
    res = []
    for i, repo in enumerate(repositories):
        if i >= top_n:
            continue
        js = dict()
        repo_full_name = repo.full_name
        js["name"] = repo_full_name
        repo_stars = repo.stargazers_count
        js["star"] = repo_stars
        repo_fork = repo.forks_count
        js["fork"] = repo_fork
        repo_watcher = repo.watchers_count
        js["watcher"] = repo_watcher
        with_readme = False
        try:
            contents = repo.get_contents("")
            for content_file in contents:
                if content_file.name.lower().startswith("readme"):
                    decoded_content = content_file.decoded_content.decode("utf-8")
                    js[content_file.name.lower()] = decoded_content
                    with_readme = True
        except:
            traceback.format_exc()
        if with_readme:
            res.append(js)

    return res


def main(index):
    df = pd.read_csv(lib_freq_path)
    g = Github(user_dict[index], token_dict[index])
    print(g.get_rate_limit())
    save_path = "data/github_search_result/{}.txt".format(index)
    save_file = open(save_path, 'a+')
    finished = get_finished_packages(index)
    for i, package_name in enumerate(df["package_name"]):
        if i % 4 == index and package_name not in finished:
            print("{}-th package: {}".format(i, package_name))
            try:
                res = search(g, package_name, 20)
                print(json.dumps({package_name: res}), file=save_file)
                time.sleep(2)
            except github.GithubException:
                print("Exceed search time rate limitation, sleep.")
                print("Before sleep, current time:", time.time())
                time.sleep(30)
                print("End sleep, current time:", time.time())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", type=int, required=True)

    args = parser.parse_args()

    search_index = args.index

    main(search_index)