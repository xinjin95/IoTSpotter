#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: analyze_maven_name_descript_result.py
@time: 7/4/21 9:58 PM
@desc:
"""
import json

result_files = ["data/search_analysis_result/data_new/search_analysis_result.txt",
                "data/search_analysis_result/data_melody/search_analysis_result.txt",
                "data/search_analysis_result/data_gpu/search_analysis_result.txt"]


def check_no_result():
    no_result = dict()
    total_pkg_names = set()
    for result_file in result_files:
        with open(result_file, 'r') as file:
            for i, line in enumerate(file):
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                total_pkg_names.add(pkg_name)
                if "no_result" in js:
                    reason = js["no_result"]
                    if reason not in no_result:
                        no_result[reason] = 0
                    no_result[reason] += 1
    print("total # of package names:", len(total_pkg_names))
    for key, val in no_result.items():
        print(key, ": ", val)


def resolve_no_result_pkgs():
    no_result = set()
    resolved_pkgs = set()
    for result_file in result_files:
        with open(result_file, 'r') as file:
            for i, line in enumerate(file):
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                if "no_result" in js:
                    no_result.add(pkg_name)
                else:
                    if "search_analysis" not in js:
                        continue
                    for res in js["search_analysis"]:
                        if "source_package_names" not in res or res["source_package_names"] == "":
                            continue
                        new_pkgs = set(res["source_package_names"].split(","))
                        resolved_pkgs.update(new_pkgs)
                        print("Add new pkgs:", len(new_pkgs))
    print("Total resolved pkgs:", len(resolved_pkgs))
    print("Total no_result pkgs:", len(no_result))
    shared = no_result.intersection(resolved_pkgs)
    print("Interception:", len(shared))
    with open("data/search_analysis_result/overall_result/cross_validate_pkgs.txt", 'w+') as file:
        for pkg_name in shared:
            print(pkg_name, file=file)


def check_found():
    visited = set()
    for result_file in result_files:
        with open(result_file, 'r') as file:
            for i, line in enumerate(file):
                js = json.loads(line)
                pkg_name = js["pkg_name"]
                if pkg_name in visited:
                    continue
                if "no_result" in js:
                    continue
                # print(js)
                with open("data/search_analysis_result/overall_result/with_search_result.txt", 'a+') as des:
                    print(json.dumps(js), file=des)


def inspect_search_result():
    non_description = 0
    match_jar = 0
    with open("data/search_analysis_result/overall_result/with_search_result.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            pom_name = ""
            pom_description = ""
            if "pom_name" in js:
                pom_name = js["pom_name"]
            if "pom_description" in js:
                pom_description = js["pom_description"]
            if pom_name != "" and pom_description == "":
                non_description += 1
            if "doc_id" in js and js["doc_id"] != "":
                match_jar += 1
                # doc_id = js["doc_id"]
            # if pom_name != "" or pom_description != "":
            #     with open("data/search_analysis_result/overall_result/with_name_description.txt", 'a+') as des:
            #         print(json.dumps(js), file=des)
    print(non_description)
    print(match_jar)

if __name__ == '__main__':
    # check_no_result()
    # resolve_no_result_pkgs()
    # check_found()
    inspect_search_result()