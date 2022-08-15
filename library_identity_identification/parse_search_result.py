#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: parse_search_result.py
@time: 6/21/21 7:17 PM
@desc:
"""
import os
import json

import pandas as pd

result_path = "data/github_search_result/search_result.txt"


def merge_results():
    with open(result_path, 'w+') as des:
        for i in range(4):
            with open("data/github_search_result/{}.txt".format(i), 'r') as src:
                for line in src:

                    try:
                        js = json.loads(line)
                    except:
                        continue
                    for value in js.values():
                        if len(value) != 0:
                            print(json.dumps(js), file=des)


def visualize_result():
    save_path = "data/github_search_result/github_search_top_1_repo_info.csv"
    # save_file = open(save_path, 'a+')
    searched_package_names, repo_names, readmes, repo_links, star_counts, fork_counts, watcher_counts = [],[],[],[],[],[],[]
    # print("searched_package_name,repo_name,readme,repo_link,star_count,fork_count,watcher_count", file=save_file)
    with open(result_path, 'r') as src:
        for line in src:
            js = json.loads(line)
            for package_name, value in js.items():
                # print(key)
                # for repo in value:
                repo = value[0]
                if "readme.md" in repo:
                    searched_package_names.append(package_name)

                    readme = repo["readme.md"]
                    readme = readme.replace(',', ' ')
                    readmes.append(readme)

                    repo_name = repo["name"]
                    repo_names.append(repo_name)

                    repo_link = "https://github.com/" + repo_name
                    repo_links.append(repo_link)

                    star_count = repo["star"]
                    star_counts.append(star_count)

                    fork_count = repo["fork"]
                    fork_counts.append(fork_count)

                    watcher_count = repo["watcher"]
                    watcher_counts.append(watcher_count)

                    # print("{},{},{},{},{},{},{}".format(package_name,
                    #                                     repo_name,
                    #                                     readme,
                    #                                     repo_link, star_count,fork_count,watcher_count), file=save_file)
    df = pd.DataFrame({"searched_package_name": searched_package_names, "repo_name": repo_names, "readme": readmes,
                       "repo_link": repo_links, "star_count": star_counts, "fork_count": fork_counts,
                       "watcher_count": watcher_counts})
    # df.to_csv(save_path, index=False)


if __name__ == '__main__':
    merge_results()
    # visualize_result()