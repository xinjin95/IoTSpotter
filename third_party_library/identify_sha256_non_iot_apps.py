#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: identify_sha256_non_iot_apps.py
@time: 7/9/21 10:45 PM
@desc:
"""
import pandas as pd
from app_url_collector.download_latest_csv import get_old_file

exclude_pkg_path = "../data/androzoo/description-improvement/xxx_xxx_shared_pkgs.txt"
save_path = "../data/androzoo/all_pkg_sha256.txt"
all_218K_pkg_name_path = "../data/androzoo/all_2182654_pkg_names.txt"
excluded_sha256_path = "data/excluded_iot_shared_sha256.csv"
all_218_sha256_path = "../data/androzoo/all_2182654_pkg_sha256.csv"


def exclude_shared():
    pkg_names = []
    shas = []
    vercodes = []
    exclude_pkgs = open(exclude_pkg_path).read().strip().split('\n')
    exclude_pkgs = set(exclude_pkgs)
    df = pd.read_csv(all_218_sha256_path)
    for i, pkg_name in enumerate(df["pkg_name"]):
        if pkg_name in exclude_pkgs:
            print("[-] did:", pkg_name)
            continue
        pkg_names.append(pkg_name)
        shas.append(df["sha256"][i])
        vercodes.append(df["vercode"][i])

    res = pd.DataFrame({"pkg_name": pkg_names, "sha256": shas, "vercode": vercodes})
    res.to_csv(excluded_sha256_path, index=False)


def read_csv():
    file_path = get_old_file(with_dir=True)
    df = pd.read_csv(file_path, compression='gzip', sep=',', quotechar='"', error_bad_lines=False)
    return df


def get_package_list():
    pkgs = []
    with open(all_218K_pkg_name_path, 'r') as src:
        for line in src:
            pkg_name = line.strip('\n')
            pkgs.append(pkg_name)
    return pkgs


def get_latest_app_info(df):
    target_packages = get_package_list()
    target_packages = set(target_packages)
    print("Total packages: ", len(target_packages))
    package_version = {}
    res = {}
    packages = df["pkg_name"]
    vercodes = df["vercode"]
    for i, package in enumerate(packages):
        print("Processing %d-th line" % i)
        if package not in target_packages:
            continue
        vercode = vercodes[i]
        try:
            version = int(vercode)
        except:
            version = 0
        if package not in package_version:
            package_version[package] = version
        if package not in res:
            res[package] = "%s,%s,%d" % (package, df["sha256"][i], version)
        max_version = package_version[package]
        if max_version < version:
            package_version[package] = version
            res[package] = "%s,%s,%d" % (package, df["sha256"][i], version)
    with open(save_path, 'w+') as file:
        print("pkg_name,sha256,vercode", file=file)
        for package, val in res.items():
            print(val, file=file)


if __name__ == '__main__':
    # get_latest_app_info(read_csv())
    exclude_shared()