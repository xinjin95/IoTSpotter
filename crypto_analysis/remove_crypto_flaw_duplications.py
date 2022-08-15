#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: remove_crypto_flaw_duplications.py
@time: 1/23/22 8:38 PM
@desc:
"""
import json

cryptoguard_path = "cryptoguard_results/cryptoguard_flaws.txt"
cryptoguard_res_path = "cryptoguard_results/cryptoguard_flaws_deduplication.txt"
cognicrypt_path = "cognicrypt_results/cognicrypt_flaws.txt"
cognicrypt_res_path = "cognicrypt_results/cognicrypt_flaws_deduplication.txt"

def find_cryptoguard_duplicates(file_path=cryptoguard_path, result_path=cryptoguard_res_path):
    with open(result_path, 'w+') as des:
        with open(file_path, 'r') as f:
            for line in f:
                js = json.loads(line)
                flaws = js['flaws']
                num_flaws = 0
                visited = set()
                new_flaws = []
                for flaw in flaws:
                    rule = flaw['rule']
                    method = ''
                    if 'method' in flaw:
                        method = flaw['method']
                    reason = ''
                    if 'reason' in flaw:
                        reason = flaw['reason']
                    identity = rule + method + reason
                    if identity not in visited:
                        num_flaws += 1
                        new_flaws.append(flaw)
                    visited.add(identity)
                js['flaws'] = new_flaws
                js['flaw_num'] = len(visited)
                print(js['app_name'], js['flaw_num'], len(visited))
                print(json.dumps(js), file=des)

def find_cognicrypt_duplicates(file_path=cognicrypt_path, result_path=cognicrypt_res_path):
    with open(result_path, 'w+') as des:
        with open(file_path, 'r') as f:
            for line in f:
                js = json.loads(line)
                flaws = js['flaws']
                num_flaws = 0
                visited = set()
                new_flaws = []
                for flaw in flaws:
                    flaw_name = ''
                    if 'flaw_name' in flaw:
                        flaw_name = flaw['flaw_name']
                    if 'rule_name' in flaw:
                        rule_name = flaw['rule_name']
                    if 'class' in flaw:
                        class_name = flaw['class']
                    method = ''
                    if 'method' in flaw:
                        method = flaw['method']
                    reason = ''
                    if 'reason' in flaw:
                        reason = flaw['reason']
                    identity = flaw_name + rule_name + class_name + method + reason
                    if identity not in visited:
                        num_flaws += 1
                        new_flaws.append(flaw)
                    visited.add(identity)
                js['flaws'] = new_flaws
                js['flaw_num'] = len(visited)
                print(js['app_name'], js['flaw_num'], len(visited))
                print(json.dumps(js), file=des)


if __name__ == '__main__':
    # find_duplicates()
    find_cognicrypt_duplicates()