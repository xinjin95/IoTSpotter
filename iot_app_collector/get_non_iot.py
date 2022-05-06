#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: fet_non_iot.py
@time: 2/2/21 10:11 AM
@desc:
"""
import json
import langid
from iot_app_collector.text_processor import TextProcessor

# metadata_path = "../data/androzoo/app_metadata.json"
metadata_path = "../data/non-iot-app/2k_apps.txt"
save_path = "../data/androzoo/2k_metadata.json"
sample_path = "../data/androzoo/20k_metadata.json"
all = []


def get_2K_apps():
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for i, line in enumerate(lines):
                # if i % 20 != 1:
                #     continue
                try:
                    pkg_name, content = line.split(":", 1)
                    js = json.loads(content)
                    all.append(js)
                    if len(all) > 2000:
                        print("write to file")
                        with open(save_path, 'a+') as des:
                            for js in all:
                                des.write(json.dumps(js) + "\n")
                        return
                    print(len(all))
                except:
                    print(line)


def get_20K_english_apps():
    total_num = 0
    tp = TextProcessor("")
    with open(metadata_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for i, line in enumerate(lines):
                # if i % 20 != 1:
                #     continue
                pkg_name, content = line.split(":", 1)
                js = json.loads(content)
                category = js["category"][0]
                tp.text = js["description"]
                res = tp.process(remove_stop_word=True)
                language = langid.classify(res)[0]
                print(language)
                if language == 'en':
                    with open(sample_path, 'a+') as des:
                        des.write(json.dumps(js) + "\n")
                    total_num += 1
                    print(total_num)
            if total_num > 20000:
                return

category_distribute = {}

def get_different_category():
    # total_num = 0
    # tp = TextProcessor("")
    with open(sample_path, 'r') as file:
        while True:
            lines = file.readlines(1000)
            if lines is None or len(lines) == 0:
                break
            for i, line in enumerate(lines):
                # if i % 20 != 1:
                #     continue
                # pkg_name, content = line.split(":", 1)
                js = json.loads(line)
                category = js["category"][0]
                # tp.text = js["description"]
                # res = tp.process(remove_stop_word=True)
                # language = langid.classify(res)[0]
                # print(language)
                # if language == 'en':
                if "GAME" in category:
                    category = "GAME"
                if category not in category_distribute.keys():
                    category_distribute[category] = []
                category_distribute[category].append(js)
    # for key, value in category_distribute.items():
    #     print(key, len(value))
    print(len(category_distribute))
    # file = open("../data/non_iot-app/different_category.txt", 'a+')
    # for i in range(30):
    #     for key, value in category_distribute.items():
    #         if len(value) > i+1:
    #             # print(key, i)
    #             # print(key, value[i])
    #             print(json.dumps(value[i]), file=file)
        # print("next")
                    # total_num += 1
                    # print(total_num)
            # if total_num > 100:
            #     for key, value in category_distribute.items():
            #         print(key, len(value))
            #     return


def generate_labeling_samples():
    file = open("../data/non-iot-app/different_category_label.csv", 'a+')
    print("pkg_name,description,developer", file=file)
    with open("../data/non-iot-app/different_category.txt", 'r') as src:
        for line in src:
            js = json.loads(line)
            des = js["description"].replace(',', ';').replace('\n', '\t')
            # developer = js["developer"]
            package_name = js["app_id"]
            title = js["title"].replace(',', ';').replace('\n', '')
            print("{},{},{},{}".format(des, 1, title, package_name), file=file)


if __name__ == '__main__':
    # get_different_category()
    # get_20K_english_apps()
    generate_labeling_samples()