#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: split_validation.py
@time: 10/19/21 8:17 PM
@desc:
"""
import json

finished_path = "../data/validation/sunil_finished_500.json"
src_metadata_path = "../data/androzoo/description-improvement/4K_shared_from_37K_metadata.txt"
todo_path = "../data/validation/todo_3500.txt"

def get_finished():
    apps = set()
    with open(finished_path, 'r') as f:
        js = json.load(f)
        for value in js.values():
            app_id = value["app_id"]
            apps.add(app_id)
        # print(len(js))
    print("Finished:", len(apps))
    return apps

def main():
    finished = get_finished()
    with open(todo_path, 'w+') as des:
        with open(src_metadata_path, 'r') as f:
            for line in f:
                js = json.loads(line)
                app_id = js["app_id"]
                if app_id in finished:
                    continue
                res = {"classified_label": 1, "app_id": app_id, "description": js["description"]}
                print(json.dumps(res), file=des)

def split():
    paths = ["xin.txt", "sunil.txt", "kaushal.txt"]
    paths = ["xin.txt", "sunil.txt"]
    with open(todo_path, 'r') as f:
        for i, line in enumerate(f):
            i = i % 2
            with open("../data/validation/" + paths[i], 'a+') as des:
                des.write(line)




if __name__ == '__main__':
    # main()
    split()