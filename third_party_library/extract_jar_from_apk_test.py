#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: extract_jar_from_apk_test.py
@time: 8/1/21 6:17 PM
@desc:
"""
import json
import os

import pandas as pd

from utility.execution import Executor
import glob
import shutil

apk_jar_dir = "/home/xxx/Documents/code/python/iot-measure/third_party_library/data/jar_extraction/apk_jar/"
src_file_path = "/home/xxx/Documents/code/python/iot-measure/third_party_library/data/iot_specific_lib_app_name_mapping/app_lib_map.txt"
apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"


def extract_jar_from_apk(apk_path, jar_path):
    app_name = os.path.basename(apk_path)
    # jar_path = save_dir + app_name + ".jar"
    exe = Executor(work_path="/home/xxx/Documents/software/dex-tools-2.1-SNAPSHOT/")
    cmd = "sh d2j-dex2jar.sh -f -o {} {}".format(jar_path, apk_path)
    # os.system(cmd)
    exe.execute(cmd)
    if os.path.exists(jar_path):
        print("\t[*] Apk to jar success")
        return True
    else:
        print("\t[-] Apk to jar failure")
        return False


def convert_apk_to_jar():
    with open(src_file_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            print("[*]", app_name)
            libs = js["app_name"]
            apk_path = apk_dir + app_name + ".apk"
            jar_path = apk_jar_dir + app_name + '.jar'
            if os.path.exists(jar_path):
                print("\t[*] finished on this app:", app_name)
                continue
            if os.path.exists(apk_path):
                extract_jar_from_apk(apk_path, jar_path)
            else:
                print("\t[-] apk not exist:", app_name)


def resolve_memory_error():
    # there was java.lang.OutOfMemoryError during running the dex2jar
    test_apps = ["marcelbd.com", "com.dteenergy.insight", "com.hualai", "com.lumiunited.aqarahome"]
    for app_name in test_apps:
        apk_path = apk_dir + app_name + ".apk"
        jar_path = apk_jar_dir + app_name + '.jar'
        extract_jar_from_apk(apk_path, jar_path)


def remove_non_target_class():
    target_apps = set()
    with open("data/jar_extraction/extraction_log.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            non_visited = js["non_visited"]
            app_name = js['app_name']
            if len(non_visited) > 0:
                target_apps.add(app_name)
    with open(src_file_path, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            pkg_names = js["libs"]
            if app_name not in target_apps:
                print("[*] Finished:", app_name)
                continue
            prefixes = get_prefix(pkg_names)
            print(app_name, ": ", prefixes)
            # if len(prefixes) > 1:
            #    dir_name = app_name
            # else:
            #    dir_name = list(prefixes)[0]
            # exe_dir = "data/jar_extraction/decompiled/" + dir_name + '/'
            exe_dir = "data/jar_extraction/decompiled/" + app_name + '/'
            if not os.path.exists(exe_dir):
                os.mkdir(exe_dir)
            exe = Executor(work_path=exe_dir)
            apk_jar_path = "../../apk_jar/" + app_name + '.jar'
            cmd = "jar -xvf {}".format(apk_jar_path)
            exe.execute(cmd)
            visited_prefixes = delete_files_by_prefix(exe_dir, prefixes)
            cmd = "jar -cvf {}.jar ../decompiled/{}/".format(app_name, app_name)
            exe = Executor(work_path="data/jar_extraction/lib_jar/")
            exe.execute(cmd)
            if os.path.exists(exe_dir):
                shutil.rmtree(exe_dir)
            with open("data/jar_extraction/extraction_log.txt", 'a+') as des:
                print(json.dumps({"app_name": app_name, "non_visited": list(prefixes.difference(visited_prefixes)),
                                  "prefix": list(prefixes), "visited": list(visited_prefixes)}), file=des)
            # files = glob.glob(exe_dir + '*', recursive=True)
            # prefixes = [prefix.replace('.', '/') for prefix in prefixes]
            # for dirpath, dirs, files in os.walk(exe_dir):
            #     # print(dirpath, dirs, files)
            #     print(dirpath)
            #     if os.path.exists(dirpath):
            #
            #         sub_dir_name = dirpath.replace(exe_dir, '')
            #
            #         matched = False
            #         for prefix in prefixes:
            #             if sub_dir_name.startswith(prefix):
            #                 matched = True
            #                 print('\t', sub_dir_name, prefix, matched)
            #                 break
            #         print('\t', sub_dir_name, matched)
            #         if not matched:
            #             shutil.rmtree(dirpath)


            # return


def delete_files_by_prefix(root_dir, prefixes):
    headers = set()
    new_prefixes = dict()
    visited = dict()
    for prefix in prefixes:
        if '.' in prefix:
            header, prefix = prefix.split('.', 1)
        else:
            header, prefix = prefix, ""
        headers.add(header)
        if header not in new_prefixes:
            new_prefixes[header] = set()
        if prefix != "":
            new_prefixes[header].add(prefix)
        # print(header, prefix)
    files = glob.glob(root_dir + '*', recursive=True)
    for file in files:
        if file == root_dir:
            continue
        relative_path = file.replace(root_dir, '')
        if not os.path.exists(file):
            continue
        if os.path.isdir(file):
            print(relative_path)
            if relative_path not in new_prefixes.keys():
                shutil.rmtree(file)
                print("remove:", file)
            else:
                if relative_path not in visited:
                    visited[relative_path] = set()
                if len(new_prefixes[relative_path]) > 0:
                    new_root_dir = file
                    if not new_root_dir.endswith('/'):
                        new_root_dir = new_root_dir + '/'
                    sub_files = glob.glob(new_root_dir + '*', recursive=True)
                    for sub_file in sub_files:
                        if sub_file == new_root_dir:
                            continue
                        sub_relative_path = sub_file.replace(new_root_dir, '')
                        if not os.path.exists(sub_file):
                            continue
                        if os.path.isdir(sub_file):
                            if sub_relative_path not in new_prefixes[relative_path]:
                                shutil.rmtree(sub_file)
                                print("remove:", sub_file)
                            else:
                                visited[relative_path].add(sub_relative_path)
                        else:
                            print(sub_relative_path)
                            # shutil.rmtree(sub_file)
                            if os.path.exists(sub_file):
                                os.remove(sub_file)
        else:
            print(relative_path)
            if os.path.exists(file):
                os.remove(file)
    visited_prefix = set()
    for key, value in visited.items():
        if len(value) == 0:
            visited_prefix.add(key)
        else:
            for v in value:
                visited_prefix.add(key + '.' + v)
    return visited_prefix


def get_iot_specific_libs():
    apps = set()
    with open("general_statistics/iot_popularity/cluster_app_mapping.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            apps = apps.union(js["apps"])
    print(len(apps))
    df = pd.read_csv("../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv")
    types = []
    for pkg_name in df["pkg_name"]:
        if pkg_name in apps:
            types.append(1)
        else:
            types.append(0)
    df["with_iot_lib"] = types
    df.to_csv("../data/androzoo/description-improvement/xxx_xxx_shared_sha256_androzoo.csv", index=False)

def get_prefix(package_names):
    prefixs = set()
    prefix_len = 2
    for pkg_name in package_names:
        lines = pkg_name.split('.')
        if len(lines) < prefix_len:
            prefix = pkg_name
        else:
            lines = lines[:prefix_len]
            prefix = '.'.join(lines)
        if prefix != "" and prefix not in prefixs:
            prefixs.add(prefix)
    return prefixs


def check_non_visited():
    total = 0
    re_runable = 0
    with open("data/jar_extraction/extraction_log.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            non_visited = js["non_visited"]
            app_name = js['app_name']
            if len(non_visited) > 0:
                print(js['app_name'])
                total += 1
                apk_path = apk_dir + app_name + ".apk"
                jar_path = apk_jar_dir + app_name + '.jar'
                if os.path.exists(jar_path):
                    os.remove(jar_path)
                if os.path.exists(apk_path):
                    extract_jar_from_apk(apk_path, jar_path)
            if len(non_visited) == len(js["prefix"]):
                re_runable += 1
    print(total)
    print(re_runable)


if __name__ == '__main__':
    # convert_apk_to_jar()
    # resolve_memory_error()
    # remove_non_target_class()
    # delete_files_by_prefix("data/jar_extraction/decompiled/com.bdtracker1/", {'com.loconav', 'io', 'com.krishna'})
    # check_non_visited()
    get_iot_specific_libs()