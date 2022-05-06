#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: parse_result.py
@time: 1/19/22 9:49 PM
@desc:
"""
import glob
import json
import os.path

import pandas as pd

from check_scheme import result_dir, get_finished, app_list_csv

finished_list = "/home/xin/Documents/code/python/iot-measure/apk_signature_scheme/data/finished_apps.txt"
csv_result_path = "/home/xin/Documents/code/python/iot-measure/apk_signature_scheme/data/scheme_result.csv"
mini_sdk_json = "/home/xin/Documents/code/python/iot-measure/data/androzoo/description-improvement/new_shared_37K_mini_sdk.json"


def parse_one_app(file_path):
    res = ['', '', '', '']
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if "(JAR signing): " in line:
                line = line.split('(JAR signing): ')
                res[0] = line[1]
            elif "(APK Signature Scheme v2): " in line:
                line = line.split("(APK Signature Scheme v2): ")
                res[1] = line[1]
            elif "(APK Signature Scheme v3): " in line:
                line = line.split("(APK Signature Scheme v3): ")
                res[2] = line[1]
            elif "(APK Signature Scheme v4): " in line:
                line = line.split("(APK Signature Scheme v4): ")
                res[3] = line[1]
    result = []
    for r in res:
        if r == 'true':
            result.append(1)
        elif r == 'false':
            result.append(0)
        else:
            result.append(0)
    return result

def get_mini_sdk():

    mini_sdk_json = "/home/xin/Documents/code/python/iot-measure/data/androzoo/description-improvement/new_shared_37K_mini_sdk.json"
    # res = {}
    # metadata_path = "/home/xin/Documents/code/python/iot-measure/data/androzoo/description-improvement/new_shared_37K_metadata.txt"
    # with open(metadata_path, 'r') as f:
    #     for line in f:
    #         js = json.loads(line)
    #         mini_sdk = js['required_android_version']
    #         res[js['app_id']] = mini_sdk

    files = glob.glob("/home/xin/Documents/code/python/iot-measure/third_party_library/data/lib_results/*")
    parsed_res = {}
    for i, file in enumerate(files):
        print(i)
        with open(file, 'r') as f:
            for line in f:
                try:
                    js = json.loads(line)
                    if 'manifest' in js:
                        packageName = js['manifest']['packageName']
                        minSdkVersion = js['manifest']['minSdkVersion']
                        parsed_res[packageName] = minSdkVersion
                except:
                    print('read error:', file)
    print(f"# of apps: {len(parsed_res)}")
    with open(mini_sdk_json, 'w') as f:
        json.dump(parsed_res, f)



def main():
    apps = []
    v1 = []
    v2 = []
    v3 = []
    v4 = []
    downloads = []
    potentials = []
    sdk_dict = {}
    with open(mini_sdk_json, 'r') as f:
        sdk_dict = json.load(f)
    # with open(finished_list, 'r') as f:
    df = pd.read_csv(app_list_csv)
    vulns = []
    mini_sdks = []
    total_users = []
    special_app = []
    for i, pkg_name in enumerate(df['app_name']):
        # for line in f:
        #     line = line.strip('\n')
        sign_path = f'{result_dir}/{pkg_name}.txt'
        if not os.path.exists(sign_path):
            continue
        result = parse_one_app(sign_path)
        apps.append(pkg_name)
        v1.append(result[0])
        v2.append(result[1])
        v3.append(result[2])
        v4.append(result[3])
        if sum(result) == 0:
            special_app.append(pkg_name)
        downloads.append(df['install_num'][i])
        if result[0] == 1 and result[1] == 0 and result[2] == 0 and result[3] == 0:
            potentials.append(1)
        else:
            potentials.append(0)
        if pkg_name in sdk_dict:
            mini_sdk = sdk_dict[pkg_name]
        else:
            mini_sdk = 100
        mini_sdks.append(mini_sdk)
        if mini_sdk < 24 and potentials[-1] == 1:
            vulns.append(1)
            total_users.append(df['install_num'][i])
        else:
            vulns.append(0)

    res = pd.DataFrame(
        {
            "app_name": apps,
            'v1': v1,
            'v2': v2,
            'v3': v3,
            'v4': v4,
            'install_num': downloads,
            'potential': potentials,
            'mini_sdk': mini_sdks,
            'vulnerable': vulns,
        }
    )

    res.to_csv(csv_result_path, index=False)
    print(f"# of vulnerable apps: {sum(vulns)}, out of {len(vulns)} apps")
    print(len(special_app), special_app)
    print(sum(potentials))
    # print(f"The vulnerabilities will affect at least {int(sum(total_users) * 0.067)} users out of {sum(downloads)}")

def get_download_dict():
    res = dict()
    df = pd.read_csv('../data/androzoo/description-improvement/shared_37K_pkg_download_rank.csv')
    for i, app in enumerate(df['app_name']):
        res[app] = df['']


def get_download_scheme_distribution():
    df = pd.read_csv(csv_result_path)
    res = dict()
    num_50k = 0
    v1 = dict()
    v2 = dict()
    v3 = dict()
    v4 = dict()
    vulnerable = dict()
    for i, download in enumerate(df['install_num']):
        if download < 100:
            download = 50
        elif download > 10000000:
            download = 50000000
        if download not in res:
            res[download] = 0
        if download not in v1:
            v1[download] = 0
        v1[download] += df['v1'][i]
        if download not in v2:
            v2[download] = 0
        v2[download] += df['v2'][i]
        if download not in v3:
            v3[download] = 0
        v3[download] += df['v3'][i]
        if download not in v4:
            v4[download] = 0
        v4[download] += df['v4'][i]
        if download not in vulnerable:
            vulnerable[download] = 0
        vulnerable[download] += df['vulnerable'][i]
        if download >= 50000:
            num_50k += 1
        res[download] += 1
    print(res)
    print(v1)
    print(v2)
    print(v3)
    print(v4)
    print(vulnerable)
    print(len(res))
    print(num_50k)
    # print(res.keys())
    print(res.keys())
    print(res.values())
    print(v1.values())
    print(v2.values())
    print(v3.values())
    print(v4.values())
    print(vulnerable.values())

def calculate_percent():
    installs = [50000000, 10000000, 5000000, 1000000, 500000, 100000, 50000, 10000, 5000, 1000, 500, 100, 50]
    all = [26, 109, 103, 679, 582, 2252, 1629, 5582, 2996, 7873, 3120, 6379, 6453]
    v1 = [20, 96, 96, 648, 548, 2156, 1574, 5399, 2892, 7604, 3014, 6084, 6089]
    v2 = [22, 97, 81, 558, 462, 1668, 1199, 4099, 2183, 5878, 2417, 5155, 5693]
    v3 = [10, 36, 39, 228, 164, 696, 487, 1859, 964, 2755, 1229, 2749, 3313]

    vuln = [3, 9, 21, 116, 114, 562, 413, 1429, 784, 1928, 668, 1140, 700]
    percent = [v/all[i]*100 for i, v in enumerate(vuln)]
    print(percent)
    print(sum(v1), sum(v2), sum(v3))


if __name__ == '__main__':
    # get_finished()
    main()
    # get_mini_sdk()
    # get_download_scheme_distribution()
    # calculate_percent()