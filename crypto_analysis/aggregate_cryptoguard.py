#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: aggregate_cryptoguard.py
@time: 10/10/21 3:34 PM
@desc:
"""
import json

import pandas as pd

src_file = "cryptoguard_results/cryptoguard_flaws_deduplication.txt"

def get_violation_per_apps():
    overall_rule = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [],
                    '11': [], '12': [], '13': [], '14': [], '15': [], '16': []}
    apps = []
    total_flaws = []
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            if app_name == "codematics.wifitv.tvremote.smarttv.remotecontrol.tv.remote.control":
                print("here")
            flaws = js["flaws"]
            rule_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0}
            flaw_num = js["flaw_num"]
            for flaw in flaws:
                rule = flaw["rule"]
                if rule == '8a':
                    rule = '8'
                # if rule not in rule_dict:
                #     print(rule)
                #     continue
                rule_dict[rule] += 1
            # print(app_name, rule_dict)
            apps.append(app_name)
            total_flaws.append(flaw_num)
            for rule, value in rule_dict.items():
                overall_rule[rule].append(value)
    # overall_rule["app_name"] = apps
    # overall_rule["total_flaw_num"] = total_flaws
    res = {"app_name": apps}
    for key, val in overall_rule.items():
        res["rule_"+key] = val
    res["total_flaw_num"] = total_flaws
    df = pd.DataFrame(res)
    df = df.sort_values("total_flaw_num", ascending=False)
    df.to_csv("cryptoguard_results/accumulated_result_for_app.csv", index=False)
    print(f"Total violations: {sum(total_flaws)}")


def get_most_popular_rule():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    df = df.loc[df["rule_13"] > 0]
    print(len(df))
    # 842


def get_app_with_max_violations():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    i = df['total_flaw_num'].argmax()
    print(df["app_name"][i])
    # com.remotefairy4
    print(df["total_flaw_num"][i])


def get_apps_with_at_lease_one_violations():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    df = df.loc[df["total_flaw_num"] > 0]
    print(len(df))
# def get_violation_per_libs():


def get_empty_rule_dict():
    res = dict()
    for i in range(1, 17):
        res[str(i)] = []
    print(res)
    return res

def get_sorted_app_by_devices():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    df = df.sort_values("total_flaw_num", ascending=False)
    device_dict = dict()
    flaw_dict = dict()
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            flaw_num = js["flaw_num"]
            IOT_PRODUCT = js["IOT_PRODUCT"]
            device_dict[app_name] = IOT_PRODUCT
            flaw_dict[app_name] = flaw_num
    with open("cryptoguard_results/app_flaws_product_ranked.txt", 'w+') as f:
        for app in df["app_name"]:
            js = {"app_name": app, "flaw_num": flaw_dict[app], "IOT_PRODUCT": device_dict[app]}
            print(json.dumps(js), file=f)


def get_package_name_from_method(method):
    # print(method)
    try:
        class_name, _ = method.split(':', 1)
        class_name = class_name.replace('<', '')
        tmp = class_name.split('.')
        if len(tmp[:-1]) < 1:
            return None
        package_name = '.'.join(tmp[:-1])
        return package_name
    except:
        print(method)
        return None


def get_violation_per_lib():
    overall_rule = dict()
    libs = []
    rule_dict = dict()
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            flaws = js["flaws"]
            # flaw_num = js["flaw_num"]
            for flaw in flaws:
                rule = flaw["rule"]
                if rule == '8a':
                    rule = '8'
                if "method" not in flaw:
                    continue
                method = flaw["method"]
                package_name = get_package_name_from_method(method)
                if package_name is None or package_name.startswith(app_name):
                    continue
                # rule_dict =
                if package_name not in overall_rule:
                    overall_rule[package_name] = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0,
                             '12': 0, '13': 0, '14': 0, '15': 0, '16': 0}
                overall_rule[package_name][rule] = overall_rule[package_name][rule] + 1
                # overall_rule[package_name] =
    total_flaws = []
    for lib, value in overall_rule.items():
        libs.append(lib)
        total = 0
        for k, v in value.items():
            if k not in rule_dict:
                rule_dict[k] = []
            rule_dict[k].append(v)
            total += v
        total_flaws.append(total)

    # libs = []
    # rule_all = dict()

    res = {"3rd_party_lib": libs}
    for key, val in rule_dict.items():
        res["rule_"+key] = val
    res["total_flaw_num"] = total_flaws
    df = pd.DataFrame(res)
    df.to_csv("cryptoguard_results/accumulated_result_for_lib.csv", index=False)


def rank_result_by_total_num_flaws():
    csv_path = "cryptoguard_results/accumulated_result_for_lib.csv"
    df = pd.read_csv(csv_path)
    df = df.sort_values("total_flaw_num", ascending=False)
    df.to_csv(csv_path, index=False)

    csv_path = "cryptoguard_results/accumulated_result_for_app.csv"
    df = pd.read_csv(csv_path)
    df = df.sort_values("total_flaw_num", ascending=False)
    df.to_csv(csv_path, index=False)


def get_app_num_per_rule():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    app_num = []
    for i in range(1, 17):
        col_name = 'rule_{}'.format(i)
        tmp = df.loc[df[col_name] > 0]
        app_num.append(str(len(tmp)))
    with open('cryptoguard_results/rule_num_apps.csv', 'w') as f:
        print('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16', file=f)
        print(','.join(app_num), file=f)

def get_flaw_num_per_rule():
    df = pd.read_csv("cryptoguard_results/accumulated_result_for_app.csv")
    rules = []
    for i in range(1, 17):
        col_name = 'rule_{}'.format(i)
        # tmp = df.loc[df[col_name] > 0]
        rules.append(str(int(df[col_name].sum())))
    with open('cryptoguard_results/flaw_num_per_rule.csv', 'w') as f:
        # print()
        print('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16', file=f)
        print(','.join(rules), file=f)


# get_empty_rule_dict()
# get_violation_per_apps()
# get_most_popular_rule()
# get_app_with_max_violations()
# get_apps_with_at_lease_one_violations()
# get_sorted_app_by_devices()
# get_violation_per_lib()
# rank_result_by_total_num_flaws()
# get_app_num_per_rule()
get_flaw_num_per_rule()