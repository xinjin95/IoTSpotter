#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: callgraph_analysis.py
@time: 12/15/21 12:24 AM
@desc:
"""
import json
import os.path
from collections import Counter

# from utility.execution import Executor
import subprocess

import pandas as pd


class Node():

    def __init__(self, sig):
        self.sig = sig
        self.caller = set()
        self.callee = set()
        self.is_iot = False

    def set_caller(self, sig):
        self.caller.add(sig)

    def set_callee(self, sig):
        self.callee.add(sig)

    def get_caller(self):
        return self.caller

    def get_callee(self):
        return self.callee

    def get_is_iot(self):
        return self.is_iot

    def set_is_iot(self, is_iot):
        self.is_iot = is_iot


class Executor(object):

    def __init__(self, print_cmd=False, timeout=None, read_lines=False, work_path=None):
        """
        :param cmd: cmd to be executed
        :param print_cmd: boolean, print cmd or not
        :param timeout: time out if not finish within timeout seconds
        """
        self.print_cmd = print_cmd
        self.timeout = timeout
        self.read_lines = read_lines
        self.work_path = work_path

    def execute(self, cmd):
        """
        execute cmd with timeout if not set as None
        :param cmd: cmd to execute
        :return: null
        """
        if self.print_cmd:
            print(cmd)
        if self.work_path is None:
            process = subprocess.Popen(cmd, shell=True)
        else:
            process = subprocess.Popen(cmd, shell=True, cwd=self.work_path)
        try:
            if self.timeout is not None:
                process.wait(timeout=self.timeout)
            else:
                process.wait()
        except subprocess.TimeoutExpired:
            process.terminate()
            print("cmd: %s timeout expired" % cmd)
            # logging.debug("cmd: %s timeout expired"%self.cmd)
            # TODO: add lib_log

    def execute_stdout(self, cmd):
        """
        execute cmd with stdout return
        :param cmd: cmd to execute
        :return: execution result
        """
        if self.print_cmd:
            print(cmd)

        if self.work_path is None:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True, cwd=self.work_path)
        try:
            if self.timeout is not None:
                outs = process.communicate(timeout=self.timeout)[0]
            else:
                outs = process.communicate()[0]
            return outs.decode("utf-8")
            #
            # print(outs)
            # print(errs)

            # if self.timeout is not None:
            #     process.wait(timeout=self.timeout)
            # else:
            #     process.wait()
            #
            # if self.read_lines:
            #     res = process.stdout.readlines()
            #     res_decode = ""
            #     for line in res:
            #         res_decode += line.decode("utf-8")
            #     return res_decode
            # else:
            #     return process.stdout.read().decode("utf-8")
        except subprocess.TimeoutExpired:
            # print(traceback.format_exc())
            print("cmd: %s timeout expired" % cmd)
            process.terminate()
            # TODO: add lib_log



def set_iot_packages():
    res = set()
    with open("data/iot_package_names.txt", 'r') as f:
        for line in f:
            line = line.strip('\n')
            res.add(line)
    return res

iot_packages = set_iot_packages()


def main():
    file_path = "/home/xxx/Documents/code/python/iot-measure/crypto_analysis/data/call_graph_analysis/iot_lib_apps.txt"
    # jar_path = "callGraphAnalzer.jar"
    jar_path = "callGraphAnalyzer_retrieve_call_chain.jar"
    apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
    exe = Executor(work_path="/home/xxx/Documents/code/python/iot-measure/crypto_analysis/data/call_graph_analysis/")
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            # if i < 94: # com.lgeha.nuts
            #     continue
            pkg_name = line.strip('\n')
            cmd = "java -jar {} {}{}.apk".format(jar_path, apk_dir, pkg_name)
            # print(cmd)
            exe.execute(cmd)


def result_analysis():
    file_path = "data/call_graph_analysis/iot_lib_apps.txt"
    res_csv_path = "data/call_graph_analysis/callgraph_analysis_result.csv"
    # with open(res_csv_path, 'w') as des:
    #     print(",Cryptoguard,,Cognitive,", file=des)
    #     print("pkg_name,num_flaws,num_flaw_iot_lib,num_flaws,num_flaw_iot_lib", file=des)
    cryptoguard_res = analyze_cryptoguard_result()
    cognitive_res = analyze_cognitive_result()
    # cry_all = []
    # cry_iot = []
    # cog_all = []
    # cog_iot = []

    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            # if i >= 94:
            #     continue
            pkg_name = line.strip('\n')
            if pkg_name not in cryptoguard_res:
                cry_all = -1
                cry_iot = -1
            else:
                cry_all = cryptoguard_res[pkg_name]["all"]
                cry_iot = cryptoguard_res[pkg_name]["iot"]

            if pkg_name not in cognitive_res:
                cog_all = -1
                cog_iot = -1
            else:
                cog_all = cognitive_res[pkg_name]["all"]
                cog_iot = cognitive_res[pkg_name]["iot"]
            # with open(res_csv_path, 'a+') as des:
            #     print("{},{},{},{},{}".format(pkg_name, cry_all, cry_iot, cog_all, cog_iot), file=des)
            # if pkg_name not in cryptoguard_res:
            #     cry_all.append(-1)
            #     cry_iot.append(-1)
            # else:
            #     cry_all.append(cryptoguard_res[pkg_name]["all"])
            #     cry_iot.append(cryptoguard_res[pkg_name]["iot"])
            #
            # if pkg_name not in cognitive_res:
            #     cog_all.append(-1)
            #     cog_iot.append(-1)
            # else:
            #     cog_all.append(cognitive_res[pkg_name]["all"])
            #     cog_iot.append(cognitive_res[pkg_name]["iot"])

def add_call_chain(call_chain, node_dict):
    if len(call_chain) > 1:
        i = 1
        while i < len(call_chain):
            pre = call_chain[i-1]
            cur = call_chain[i]
            pre_node = create_node(pre, node_dict)
            cur_node = create_node(cur, node_dict)
            pre_node.set_caller(cur_node)
            cur_node.set_callee(pre_node)
            i += 1
    return node_dict

def create_node(sig, node_dict):
    if sig not in node_dict:
        node = Node(sig)
        node.set_is_iot(check_is_iot(sig))
        node_dict[sig] = node
    return node_dict[sig]

def check_is_iot(sig):
    class_name = sig.split(':')[0]
    class_name = class_name[1:]
    class_name = class_name.split('.')
    class_name = class_name[:-1]
    class_name = '.'.join(class_name)
    is_iot = class_name in iot_packages
    return is_iot


def analyze_cryptoguard_result():
    res = dict()
    node_dict = dict()
    with open("data/call_graph_analysis/cryptoguard/cryptoguard_flaws.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js['app_name']
            total_flaws = js["flaw_num"]
            flaws = js['flaws']
            num_iot_flaws = 0
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    num_iot_flaws += 1
                    # call_chain = flaw['call_chain']
                    # add_call_chain(call_chain, node_dict)
            res[app_name] = {"all": total_flaws, "iot": num_iot_flaws}
    return res

def call_chain_cryptoguard():

    with open("data/call_graph_analysis/cryptoguard/cryptoguard_flaws.txt", 'r') as f:
        for line in f:
            node_dict = dict()
            js = json.loads(line)
            flaws = js['flaws']
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    call_chain = flaw['call_chain']
                    add_call_chain(call_chain, node_dict)
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    call_chain = flaw['call_chain']
                    last = call_chain[-1]
                    is_iot = check_is_iot(last)
                    if not is_iot:
                        # node = node_dict[last]
                        # print("here")
                        path = get_call_chain(last, [], node_dict)
                        print(path)

def get_call_chain(sig, path, node_dict):
    node = node_dict[sig]
    path.append(sig)
    if len(node.get_caller()) > 0:
        for caller in node.get_caller():
            if is_iot_chain(caller, path, node_dict):
                return path
    return []

def is_iot_chain(node, path, node_dict):
    path.append(node.sig)
    is_iot = node.get_is_iot()
    if is_iot:
        return is_iot
    else:
        for caller in node.get_caller():
            is_iot = is_iot or is_iot_chain(caller, path, node_dict)
            if is_iot:
                break
        if not is_iot:
            del path[-1]
        return is_iot


def analyze_cognitive_result():
    res = dict()
    with open("data/call_graph_analysis/cognitive/cognicrypt_flaws.txt", 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js['app_name']
            total_flaws = js["flaw_num"]
            flaws = js['flaws']
            num_iot_flaws = 0
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    num_iot_flaws += 1
            res[app_name] = {"all": total_flaws, "iot": num_iot_flaws}
    return res

def deduplicate(input_list):
    input_list = set(input_list)
    input_list = list(input_list)
    input_list = '\n'.join(input_list)
    return input_list

def call_chain_analysis():
    csv_file = "data/call_graph_analysis/cognitive/cognicrypt_flaws_call_chain.csv"
    src_file = "data/call_graph_analysis/cognitive/cognicrypt_flaws_call_chain.txt"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    # counter = Counter()
    # with open("data/call_graph_analysis/cognitive/cognicrypt_flaws_call_chain.txt", 'r') as f:
    # file = open("data/call_graph_analysis/cryptoguard/cryptoguard_flaws_call_chain.csv", 'a+')
    # print("app_name,rule_id,method,call_chain,iot_product,protocol", file=file)
    app_names = []
    products = []
    protocols = []
    rule_ids = []
    call_chains = []
    methods = []
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js['app_name']

            total_flaws = js["flaw_num"]
            flaws = js['flaws']
            num_iot_flaws = 0
            product = deduplicate(js['IOT_PRODUCT'])
            protocol = deduplicate(js['PROTOCOL'])




            # counter.update([app_name])
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    # num_iot_flaws += 1
                    # method = flaw['method']
                    # rule_id = flaw['rule']
                    rule_id = flaw['flaw_name']
                    call_chain = flaw['call_chain']
                    method = call_chain[0]
                    call_chain = '\n'.join(call_chain)
                    # print(f'{app_name},{rule_id},{method},{call_chain},{product},{protocol}', file=file)

                    app_names.append(app_name)
                    products.append(product)
                    protocols.append(protocol)

                    rule_ids.append(rule_id)
                    methods.append(method)
                    call_chains.append(call_chain)
    # print(counter)
    # file.close()
    df = pd.DataFrame({
        'app_name': app_names,
        'rule_name': rule_ids,
        'flaw_method': methods,
        'call_chain': call_chains,
        # 'IoT_product': products,
        # 'IoT_protocol': protocols
    })
    df.to_csv(csv_file, index=False)

def dump_iot_method():
    src_file = "data/call_graph_analysis/cognitive/cognicrypt_flaws_call_chain.txt"
    cognicrypt_methods = get_iot_methods(src_file)
    src_file = "data/call_graph_analysis/cryptoguard/cryptoguard_flaws_call_chain.txt"
    cryptoguard_methods = get_iot_methods(src_file)
    all = cryptoguard_methods.union(cognicrypt_methods)
    # print(call_chain)

    with open("data/call_graph_analysis/iot_methods_to_confirm.txt", 'w') as des:
        for line in all:
            print(line, file=des)


def get_iot_methods(src_file):
    res = set()
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js['app_name']

            total_flaws = js["flaw_num"]
            flaws = js['flaws']
            for flaw in flaws:
                if "is_iot" in flaw and flaw["is_iot"] == 1:
                    call_chain = flaw['call_chain']
                    iot_method = call_chain[-1]
                    res.add(iot_method)
    return res

if __name__ == '__main__':
    # main()
    # result_analysis()
    # call_chain_cryptoguard()
    # call_chain_analysis()
    dump_iot_method()