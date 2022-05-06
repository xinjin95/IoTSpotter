#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_apps_containing_iot_libs.py
@time: 8/2/21 11:32 PM
@desc:
"""
import pandas as pd
import json
import os
from classification.dictionary import Dictionary

csv_path = "data/xin_sunil_shared_sha256_androzoo.csv"
iot_csv_paths = ["data/iot_specific_lib_filter/both_exist_filtered.csv",
                 "data/iot_specific_lib_filter/only_in_iot_filtered.csv"]


def collect_iot_package_names() -> set:
    iot_pkgs = set()
    for iot_csv_path in iot_csv_paths:
        df = pd.read_csv(iot_csv_path)
        package_names = set(df["package_name"])
        iot_pkgs = iot_pkgs.union(package_names)
    return iot_pkgs


def get_lib_per_app(result_path):
    with open(result_path, 'r') as file:
        for line in file:
            try:
                js = json.loads(line)
                return js['thirdPartyLibs'].keys()
            except:
                return set([])


def map_package_name_with_app_name():
    iot_package_names = collect_iot_package_names()
    print(f'# of iot package names: {len(iot_package_names)}')
    if os.path.exists("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt"):
        os.remove("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt")
    lib_app_map = dict()
    for lib in iot_package_names:
        lib_app_map[lib] = set()
    df = pd.read_csv(csv_path)
    for i, pkg_name in enumerate(df["pkg_name"]):
        result_path = "data/lib_results/" + pkg_name + ".txt"
        print("{}-th: {}".format(i, pkg_name))
        if os.path.isfile(result_path):
            libs = get_lib_per_app(result_path)
            intersect = iot_package_names.intersection(libs)
            print("intersect:", len(intersect))
            for lib in intersect:
                lib_app_map[lib].add(pkg_name)
            #for lib in libs:
            #    if lib in iot_package_names:
            #        lib_app_map[lib].add(pkg_name)
    with open("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt", 'a+') as f:
        for lib, apps in lib_app_map.items():
            js = {"package_name": lib, "apps": list(apps)}
            print(json.dumps(js), file=f)


def get_top_app_lib_mapping():
    iot_package_names = collect_iot_package_names()
    print(f'# of iot package names: {len(iot_package_names)}')
    apps = open("/home/xin/Documents/code/python/iot-measure/crypto_analysis/data/call_graph_analysis/iot_lib_apps.txt", 'r').read().strip().split('\n')
    print(f"# of apps:{len(apps)}")
    with open("../crypto_analysis/data/iot_app_lib_mapping.txt", 'w') as f:
        for pkg_name in apps:
            result_path = "data/lib_results/" + pkg_name + ".txt"
            if os.path.isfile(result_path):
                libs = get_lib_per_app(result_path)
                intersect = iot_package_names.intersection(libs)
                print(f"{pkg_name}: # of libs {len(intersect)}")
                print(json.dumps({"app_id": pkg_name, "iot_specific_packages": list(intersect)}), file=f)
            else:
                print(pkg_name, 'null')

def check_every_package_name_has_corresponding_apk():
    with open("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            if len(js["apps"]) == 0:
                print(js["package_name"])


def get_total_apps():
    total_apps = set()
    with open("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            total_apps = total_apps.union(set(js["apps"]))
    print(f'total apps: {len(total_apps)}')
    with open("../library_scan/flowdroid/data/target_apps.txt", 'w+') as des:
        for app in total_apps:
            print(app, file=des)


def get_iot_app_download_dict():
    res = dict()
    with open('../data/androzoo/description-improvement/new_shared_37K_metadata.txt', 'r') as f:
        for line in f:
            js = json.loads(line)
            app_id = js["app_id"]
            install = js["installs"]
            install = install.replace('+', '').replace(',', '')
            install = int(install)
            res[app_id] = install
    dictionary = Dictionary(res)
    return dictionary.sort_by_value()


def select_top_install_app_from_mapping():
    app_install_dict = get_iot_app_download_dict()
    with open("data/iot_specific_lib_app_name_mapping/iot_lib_map.txt", 'r') as src:
        for line in src:
            js = json.loads(line)
            package_name, apps = js["package_name"], js["apps"]
            dictionary = {app_id: app_install_dict[app_id] for app_id in apps}
            dictionary = Dictionary(dictionary)
            apps = dictionary.sort_by_value()
            print(apps)
            js = {"package_name": package_name, "apps": list(apps.keys())}
            with open("data/iot_specific_lib_app_name_mapping/iot_lib_map_ranked.txt", 'a+') as des:
                print(json.dumps(js), file=des)


def select_top_app_to_csv():
    package_names = []
    top_apps = []
    with open("data/iot_specific_lib_app_name_mapping/iot_lib_map_ranked.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            package_name = js["package_name"]
            apps = js["apps"]
            top_app = apps[0]

            package_names.append(package_name)
            top_apps.append(top_app)
    df = pd.DataFrame({"package_name": package_names, "app_name": top_apps})
    df.to_csv("data/iot_specific_lib_app_name_mapping/iot_lib_top_app.csv", index=False)


def group_lib():
    df = pd.read_csv("data/iot_specific_lib_app_name_mapping/iot_lib_top_app.csv")
    res = dict()
    for i, app_name in enumerate(df["app_name"]):
        if app_name not in res:
            res[app_name] = set()
        res[app_name].add(df["package_name"][i])
    with open("data/iot_specific_lib_app_name_mapping/app_lib_map.txt", 'w+') as f:
        for app_name, libs in res.items():
            print(json.dumps({"app_name": app_name, "libs": list(libs)}), file=f)


if __name__ == '__main__':
    # map_package_name_with_app_name()
    # get_total_apps()
    # check_every_package_name_has_corresponding_apk()
    # select_top_install_app_from_mapping()
    # select_top_app_to_csv()
    # group_lib()
    get_top_app_lib_mapping()