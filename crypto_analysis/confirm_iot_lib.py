#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: confirm_iot_lib.py
@time: 1/11/22 11:09 AM
@desc:
"""
import shutil
src_file = "data/call_graph_analysis/iot_methods_to_confirm.txt"
non_iot_file = "data/call_graph_analysis/confirm_iot_lib/confirmed_noniot_list.txt"
confirmed_file = "data/call_graph_analysis/confirm_iot_lib/confirmed_lib_list.txt"
res_file = "data/call_graph_analysis/confirm_iot_lib/reminding_file.txt"
tmp_file = "data/call_graph_analysis/confirm_iot_lib/tmp.list.txt"

def get_confirmed_list(file_path):
    res = set()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            res.add(line)
    return res

def get_methods():
    confirmed_list = get_confirmed_list(confirmed_file)
    confirmed_list = confirmed_list.union(get_confirmed_list(non_iot_file))
    shutil.copy(res_file, tmp_file)
    with open(res_file, 'w') as des:
        with open(tmp_file, 'r') as f:
            for line in f:
                line = line.strip('\n')
                confirmed = False
                for list in confirmed_list:
                    if line.startswith(list):
                        confirmed = True
                        break
                if not confirmed:
                    print(line, file=des)

# shutil.copy(src_file, res_file)
get_methods()