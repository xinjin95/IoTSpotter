#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: exclude_common_libs.py
@time: 6/25/21 11:57 PM
@desc:
"""
from pygtrie import StringTrie
import pandas as pd
import os


def read_packages(path_to_file):
    res = []
    if path_to_file.endswith('.txt'):
        res = open(path_to_file, 'r').read().strip().split('\n')
    elif path_to_file.endswith('.csv'):
        df = pd.read_csv(path_to_file)
        res = df["package_name"]
    else:
        print("invalid file")
    return res


def create_trie(package_list):
    trie = StringTrie(separator='.')
    print("============== Create trie ================")
    for pkg in package_list:
        # print("[-]", pkg)
        trie[pkg] = 1
    return trie


def main():
    all_package_path = "/home/xin/Documents/code/python/iot-measure/third_party_library/data/lib_frequency.csv"
    all_pkg_list = read_packages(all_package_path)
    all_pkg_list = list(set(all_pkg_list))
    print("Total # of 3rd-party-libs:", len(all_pkg_list))
    all_pkg_trie = create_trie(all_pkg_list)

    # ads packages
    ads_pkg_paths = ["data/common_libraries/CommonLibraries/libraries/ad_240.txt",
                     "data/common_libraries/CommonLibraries/libraries/ad_1050.txt"]
    ads_package_list = read_packages(ads_pkg_paths[0]) + read_packages(ads_pkg_paths[1])
    ads_package_list = list(set(ads_package_list))
    print("Total # of ads libs:", len(ads_package_list))
    # ads_pkg_file = open("data/common_libraries/iot_libs/ads_package_names.txt", 'a+')

    # common libs
    # get common_packages file path
    common_pkg_paths = []
    _, _, filenames = next(os.walk("data/common_libraries/CommonLibraries/libraries"))
    for filename in filenames:
        if filename.startswith("ad_"):
            continue
        common_pkg_paths.append("data/common_libraries/CommonLibraries/libraries/" + filename)

    # read package names
    common_pkg_list = []
    for pkg_path in common_pkg_paths:
        common_pkg_list = common_pkg_list + read_packages(pkg_path)
    common_pkg_list = set(common_pkg_list)
    print("Total # of common libs:", len(common_pkg_list))

    # get the packages starting with the prefix
    common_pkg_file = open("data/common_libraries/iot_libs/common_package_names.txt", 'a+')
    for pkg in common_pkg_list:
        if all_pkg_trie.has_subtrie(pkg):
            # res1 = all_pkg_trie[pkg]
            res2 = all_pkg_trie.iterkeys(prefix=pkg)
            for r in res2:
                # print(r, file=ads_pkg_file)
                print(r, file=common_pkg_file)
            # print(pkg)


def get_exclude_result():
    ads_path = "data/common_libraries/iot_libs/ads_package_names.txt"
    common_path = "data/common_libraries/iot_libs/common_package_names.txt"
    exclude_packages = []
    exclude_packages += read_packages(ads_path)
    exclude_packages += read_packages(common_path)
    exclude_packages = set(exclude_packages)
    df = pd.read_csv("../third_party_library/data/lib_frequency.csv")
    res_pkg_names = []
    res_freq = []
    for i, pkg_name in enumerate(df["package_name"]):
        if pkg_name in exclude_packages:
            continue
        res_pkg_names.append(pkg_name)
        res_freq.append(df["frequency"][i])
    df = pd.DataFrame({"package_name": res_pkg_names, "frequency": res_freq})
    df.to_csv("data/common_libraries/iot_libs/exclusion_res.csv", index=False)


if __name__ == '__main__':
    # main()
    get_exclude_result()