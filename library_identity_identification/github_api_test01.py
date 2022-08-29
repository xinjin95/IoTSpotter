#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: github_api_test01.py
@time: 6/21/21 12:19 AM
@desc:
"""
from github import Github

token_dict = {"xxxxxx95": "xxxxxx",
              "xxxxxx": "xxxxxx",
              "xxxxxx": "xxxxxx",
              "xxxxxx": "xxxxxx"}


g = Github("xxxxxx", "xxxxxx")
print(g.get_rate_limit())
user = g.get_user("xxxxxx95")
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# for repo in g.get_user().get_repos():
#     print(repo.name)

repositories = g.search_repositories(query='android.support.v4.app')
for i, repo in enumerate(repositories):
    # print(repo)
    repo.watchers_count
    repo_full_name = repo.full_name
    contents = repo.get_contents("")
    for content_file in contents:
        if content_file.name.lower().startswith("readme"):
            decoded_content = content_file.decoded_content.decode("utf-8")

        print(content_file)