#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: parse_cognicrypt_results..py
@time: 10/6/21 10:57 AM
@desc:
"""
import glob
import json
import os
import ast
from parse_cryptoguard_results import load_ner_results

def main():
    ner_dict = load_ner_results()
    root_dir = "data/cognicrypt_results_over1m/"
    files = glob.glob(root_dir + '*')
    while len(files) > 0:
        file = files.pop()
        if os.path.isdir(file):
            # print(file)
            if "piped_logs_" in file:
                continue
            if not file.endswith('/'):
                file = file + '/'
            new_files = glob.glob(file + '*')
            files = files + new_files
        else:
            if file.endswith('CogniCrypt-Report.txt'):
                parse_each_result(file, ner_dict)


def parse_each_result(file, ner_dict):
    with open("cognicrypt_results/cognicrypt_flaws.txt", 'a+') as des:
        flaws = []
        className = ""
        methodName = ""
        prev_line = ""
        with open(file, 'r') as f:
            for line in f:

                line = line.strip('\n').replace('\t', '')
                # print(line)
                if "Findings in Java Class: " in line:
                    className = line.replace("Findings in Java Class: ", '')
                elif "in Method: " in line:
                    _, methodName = line.split("in Method: ", 1)
                elif " violating CrySL rule for " in line:
                    flawName, ruleName = line.split(" violating CrySL rule for ", 1)

                elif "at statement: " in line:
                    _, statement = line.split("at statement: ", 1)
                    reason = prev_line
                    js = {"flaw_name": flawName, "rule_name": ruleName, "class": className, "method": methodName,
                          "statement": statement, "reason": reason}
                    flaws.append(js)
                    # print(js)
                    # if "data/" in reason:
                    #     print("here")
                    # print(reason)
                prev_line = line

        files = file.split('/')
        app_name = files[-2]
        folder = files[2].replace('_logs', '')
        try:
            entity = ner_dict[app_name]
        except:
            app_name = "com.newpower.apkmanager"
            entity = ner_dict[app_name]
            # print(file)
            # return
        js = {"app_name": app_name, "folder": folder, "flaw_num": len(flaws), "flaws": flaws,
              "IOT_PRODUCT": entity["IOT_PRODUCT"],
              "PROTOCOL": entity["PROTOCOL"]}
        print(json.dumps(js), file=des)


if __name__ == '__main__':
    main()