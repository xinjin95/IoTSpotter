#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: collect_statistics_top_libs.py
@time: 8/24/21 11:10 PM
@desc:
"""
import glob
import json
import os
import pandas as pd
import zipfile

csv_path = "general_statistics/top_libs/general_iot_statistics - top_libraries.csv"


def get_libs() -> list:
    df = pd.read_csv(csv_path)
    libs = list(df["Library"])
    print("# of libs:", len(libs))
    return libs


def get_target_apps():
    apps = set()
    df = pd.read_csv("../data/androzoo/description-improvement/xin_sunil_shared_sha256_androzoo.csv")
    for i, with_iot_lib in enumerate(df["with_iot_lib"]):
        if with_iot_lib == 1:
            apps.add(df["pkg_name"][i])
    # with open("../data/androzoo/description-improvement/xin_sunil_shared_sha256_androzoo.csv", 'r') as f:
    #     for line in f:
    #         js = json.loads(line)
    #         with_iot_lib = js["with_iot_lib"]
    #         if with_iot_lib == 1:
    #             apps.add(js["pkg_name"])
    print("# of apps:", len(apps))
    return apps


def main():
    apps = get_target_apps()
    libs = get_libs()
    result = dict()
    popularity = dict()
    for lib in libs:
        result[lib] = dict()
        popularity[lib] = set()
    for i, app in enumerate(apps):
        print(i, app)
        # if i > 100:
        #     continue
        app_path = "data/lib_results/" + app + '.txt'
        if os.path.exists(app_path):
            with open(app_path, 'r') as src:
                for line in src:
                    try:
                        js = json.loads(line)
                        thirdPartyLibs = js["thirdPartyLibs"]
                        for thirdPartyLib, classes in thirdPartyLibs.items():
                            for lib in libs:
                                if thirdPartyLib.startswith(lib):
                                    popularity[lib].add(app)
                                    if thirdPartyLib not in result[lib]:
                                        result[lib][thirdPartyLib] = set(classes)
                                    else:
                                        result[lib][thirdPartyLib] = result[lib][thirdPartyLib].union(set(classes))
                    except:
                        print("[-] json read error:", app)
        else:
            print("[-] no exist:", app_path)
    print(result)
    for key, value in result.items():
        for k, v in value.items():
            result[key][k] = list(v)
    with open("general_statistics/top_libs/top_lib_classes.json", 'w') as f:
        f.write(json.dumps(result))
    for key, value in popularity.items():
        popularity[key] = list(value)
    with open("general_statistics/top_libs/popularity.json", 'w') as f:
        f.write(json.dumps(popularity))


def collect_class_pkg_names():
    with open("general_statistics/top_libs/top_lib_classes.json", 'r') as f:
        for line in f:
            js = json.loads(line)
            for key, value in js.items():
                total_pkgs = len(value.keys())
                total_classes = 0
                for k, v in value.items():
                    total_classes += len(v)
                # print(key, total_pkgs, total_classes)
                # print(total_pkgs)
                print(total_classes)


def collect_popularity():
    with open("general_statistics/top_libs/popularity.json", 'r') as f:
        for line in f:
            js = json.loads(line)
            for key, value in js.items():
                print(key, len(value))
                # print(len(value))


def check_tutk():
    pkg_name = "com.tutk"
    jar_files = glob.glob("/home/xin/Documents/code/python/iot-measure/mvncrawler/maven/tuya/jars/*")
    for jar_file in jar_files:
        try:
            if not jar_file.endswith('.jar'):
                continue
            zip = zipfile.ZipFile(jar_file)
            files = zip.namelist()
            # print(files)
            for file in files:
                if not file.endswith('.class'):
                    continue
                base_name = '/' + os.path.basename(file)
                class_path = file.replace(base_name, '')
                class_path = class_path.replace('/', '.')
                if class_path.startswith(pkg_name):
                    print(jar_file, class_path)

        except:
            print("")


def merge_tuya_tutk():
    apps = set()
    with open("general_statistics/top_libs/popularity.json", 'r') as f:
        for line in f:
            js = json.loads(line)
            for key, value in js.items():
                if "tuya" in key or "tutk" in key:
                    apps = apps.union(set(value))
    print(len(apps))


if __name__ == '__main__':
    # main()
    # collect_class_pkg_names()
    # collect_popularity()
    # check_tutk()
    merge_tuya_tutk()