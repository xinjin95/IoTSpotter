#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: github_api_test01.py
@time: 6/21/21 12:19 AM
@desc:
"""
from github import Github

token_dict = {"xinjin95": "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",
              "autosign01": "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",
              "autosign02": "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",
              "autosign03": "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"}


g = Github("autosign01", "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")
print(g.get_rate_limit())
user = g.get_user("xinjin95")
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