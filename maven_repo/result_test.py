#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: result_test.py
@time: 6/28/21 12:50 AM
@desc:
"""
import json
import os.path
import requests
from execution import Executor
from bs4 import BeautifulSoup

result_file_path = "data/search_result.txt"
pom_dir = "data/pom/"
source_jar_dir = "data/source_jar/"
log_path = "data/package_match_log.txt"
search_analysis_result_path = "data/search_analysis_result.txt"


def download(url, local_file_name):
    if os.path.isfile(local_file_name):
        return 1
    with requests.get(url, stream=True) as r:
        print(url, r.status_code)
        if r.status_code != 404:
            r.raise_for_status()
        with open(local_file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                # shutil.copyfileobj(r.raw, f)
    if os.path.isfile(local_file_name):
        return 1
    else:
        return r.status_code


def search_package_name(local_file_name):
    res_pkgs = set()
    if not os.path.isfile(local_file_name):
        return res_pkgs
    cmd = 'zipgrep "package " {}'.format(local_file_name)
    exe = Executor()
    res = exe.execute_stdout(cmd)
    # if "ch.qos.logback.classic;" in res:
    #     print("target here")
    res = res.split('\n')
    res = set(res)

    for r in res:
        if r == "" or ':' not in r:
            continue
        r = r.split(':', 1)
        if not r[1].startswith("package "):
            continue
        r[1] = r[1].strip()
        if r[0].endswith(".java"):
            res_pkgs.add(r[1][8:-1])
            # print(r[1], r[1][8:-1])
        elif r[0].endswith(".kt"):
            res_pkgs.add(r[1][8:])
            # print(r[1], r[1][8:])
    os.remove(local_file_name)
    return res_pkgs


def process_pom_file(path_to_pom):
    pom_name = ""
    pom_description = ""

    if not os.path.isfile(path_to_pom):
        return pom_name, pom_description
    pom_file = open(path_to_pom, 'rb').read()
    soup = BeautifulSoup(pom_file)

    for n in soup.find_all('name'):
        if n.parent.name == 'project' or n.parent.name == 'parent':
            pom_name = n.get_text()
            break

    for d in soup.find_all('description'):
        if d.parent.name == 'project' or d.parent.name == 'parent':
            pom_description = d.get_text()
            break
    return pom_name, pom_description


def get_finished() -> set:
    finished = set()
    if not os.path.isfile(search_analysis_result_path):
        return finished
    with open(search_analysis_result_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["pkg_name"]
            finished.add(pkg_name)
    return finished


def main():
    finished = get_finished()
    print("finished: {}".format(len(finished)))
    with open(result_file_path, 'r') as file:
        for line in file:
            pkg_name, content = line.split(':', 1)
            if pkg_name in finished:
                print("[*] finished:", pkg_name)
                continue
            js = json.loads(content)
            if "response" not in js:
                continue
            jar_set = set()
            # source_jar_list = []
            # pom_list = []
            if "numFound" not in js["response"]:
                continue
            numFound = js["response"]["numFound"]
            if numFound == 0:
                continue
            if "docs" not in js["response"]:
                continue
            docs = js["response"]["docs"]
            doc_js_list = []
            target_doc_id = ""
            target_pom_local = ""
            target_pom_description = ""
            target_pom_name = ""
            for doc in docs:
                if "id" not in doc:
                    continue
                doc_id = doc["id"]
                version = doc["v"]
                jar_name = doc["g"] + ":" + doc["a"]
                if jar_name not in jar_set:
                    doc_js = dict()
                    doc_js["doc_id"] = doc_id
                    dir_name = doc["g"].replace('.', '/') + '/' + doc["a"] + '/' + version
                    source_short_name = doc["a"] + "-" + version + "-sources.jar"
                    source_full_name = dir_name + '/' + source_short_name
                    doc_js["source_remote"] = source_full_name
                    source_local_name = doc["g"] + "_" + doc["a"] + '_' + version + '_' + source_short_name
                    doc_js["source_local"] = source_local_name
                    pom_short_name = doc["a"] + "-" + version + ".pom"
                    pom_full_name = dir_name + '/' + pom_short_name
                    doc_js["pom_remote"] = pom_full_name
                    pom_local_name = doc["g"] + "_" + doc["a"] + '_' + version + '_' + pom_short_name
                    doc_js["pom_local"] = pom_local_name
                    source_url = 'https://search.maven.org/remotecontent?filepath=' + source_full_name
                    doc_js["source_download"] = download(source_url, source_jar_dir + source_local_name)
                    if doc_js["source_download"] != 1:
                        print("{] download failure".format(source_full_name))
                        continue
                    res_package_names = search_package_name(source_jar_dir + source_local_name)
                    doc_js["source_package_names"] = ",".join(res_package_names)
                    if pkg_name in res_package_names:
                        pom_url = 'https://search.maven.org/remotecontent?filepath=' + pom_full_name
                        doc_js["pom_download"] = download(pom_url, pom_dir + pom_local_name)

                        target_doc_id = doc_id
                        target_pom_local = pom_local_name
                        target_pom_name, target_pom_description = process_pom_file(pom_dir + pom_local_name)
                    doc_js_list.append(doc_js)
                    # print("")
                jar_set.add(jar_name)
            package_js_res = {"pkg_name": pkg_name,
                              "pom_name": target_pom_name,
                              "pom_description": target_pom_description,
                              "pom_local_path": target_pom_local,
                              "doc_id": target_doc_id,
                              "search_analysis": doc_js_list}
            with open(search_analysis_result_path, 'a+') as des:
                print(json.dumps(package_js_res), file=des)


if __name__ == '__main__':
    main()