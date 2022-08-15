#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: parse_cryptoguard_results.py
@time: 10/4/21 3:43 PM
@desc:
"""
import glob
import json
import os
import ast

def load_ner_results():
    res = dict()
    with open("data/ner_results/with_entities.jsonl", 'r') as f:
        for line in f:
            js = json.loads(line)
            name = js["name"]
            entities = js["entities"]
            entity_dict = {"IOT_PRODUCT":[], "PROTOCOL": []}
            for entity in entities:
                # print(entity)
                entity_key = entity[1]
                entity_val = entity[0]
                entity_dict[entity_key].append(entity_val)
            res[name] = entity_dict
    return res



def main():
    ner_dict = load_ner_results()
    root_dir = "data/cryptoguard_results_over1m/"

    files = glob.glob(root_dir + '*')
    apk_num = 0
    while len(files) > 0:
        file = files.pop()
        if os.path.isdir(file):
            # print(file)
            if not file.endswith('/'):
                file = file + '/'
            new_files = glob.glob(file + '*')
            files = files + new_files
        else:
            if file.endswith('.md'):
                parse_each_result(file, ner_dict)
    print(apk_num)


def parse_each_result(file, ner_dict):
    with open("cryptoguard_results/cryptoguard_flaws.txt", 'a+') as des:
        flaws = []
        # print(file)
        if "androidesko.android.electronicthermometer.apk.md" in file:
            print("stop at here")
        with open(file, 'r') as f:
            data = f.read()
            data = data.replace('\n[UnitContainer', '[UnitContainer')
            lines = data.split('\n')
            for line in lines:
                line = line.strip('\n')
                if line.startswith("***Violated Rule "):
                    line = line.replace("***Violated Rule ", '')
                    rule_num, reason = line.split(':', 1)
                    if " Found in " in reason:
                        reason, position = reason.split(" Found in ", 1)
                        position = position.strip('\n')
                        js = {"rule": rule_num, "method": position, "reason": reason}
                        flaws.append(js)
                    elif " ***Constants: " in reason:
                        reason, constants = reason.split(" ***Constants: ", 1)
                        constants = constants.strip('\n')
                        try:
                            constants = ast.literal_eval(constants)
                        except:
                            # pass
                            if "UnitContainer" in constants:
                                # pass
                                locations = constants.split('}, UnitContainer')
                                for location in locations:
                                    _, method = location.split('method=', 1)
                                    if method.endswith('}]'):
                                        method = method[:-2]
                                    method = method.strip('\'')
                                    # print(method)
                                    js = {"rule": rule_num,"method": method}
                                    flaws.append(js)
                            else:
                                # print(rule_num, constants)
                                pass

                    elif " method of " in reason:
                        method, className = reason.split(" method of ", 1)
                        className = className.strip('\n')
                        if 'in' in method:
                            _, method = method.split(" in ", 1)
                        js = {"rule": rule_num, "class": className, "method": method, "reason": reason}
                        flaws.append(js)
                    else:
                        # if ""
                        # print(reason)
                        js = {"rule": rule_num, "reason": reason}
                        flaws.append(js)
            app_name = os.path.basename(file).replace('.apk.md', '')
            folder = file.split('/')[-2]
            entity = ner_dict[app_name]
            js = {"app_name": app_name, "folder": folder, "flaw_num": len(flaws), "flaws": flaws,
                  "IOT_PRODUCT": entity["IOT_PRODUCT"],
                  "PROTOCOL": entity["PROTOCOL"]}
            print(json.dumps(js), file=des)
                    # elif "***Constants:" in reason:
                    #     reason, constants = reason.split(" ***Constants: ", 1)
                    #     constants = constants.strip('\n')

def parse_every_result(file, ner_dict):
    with open("cryptoguard_results/flaws.txt", 'a+') as des:
        flaws = []
        with open(file, 'r') as f:
            for line in f:
                if line.startswith("***Violated Rule "):
                    line = line.replace("***Violated Rule ", '')
                    rule_num, reason = line.split(':', 1)
                    if " Found in " in reason:
                        reason, position = reason.split(" Found in ", 1)
                        position = position.strip('\n')
                        js = {"rule": rule_num, "method": position, "reason": reason}
                    elif " ***Constants: " in reason:
                        reason, constants = reason.split(" ***Constants: ", 1)
                        constants = constants.strip('\n')
                        try:
                            constants = ast.literal_eval(constants)
                        except:
                            pass
                        js = {"rule": rule_num, "constants": constants, "reason": reason}
                        # constants = json.loads(constants)
                    elif " method of " in reason:
                        method, className = reason.split(" method of ", 1)
                        className = className.strip('\n')
                        if 'in' in method:
                            _, method = method.split(" in ", 1)
                        js = {"rule": rule_num, "class": className, "method": method, "reason": reason}
                    else:
                        js = {"rule": rule_num, "reason": reason}
                    flaws.append(js)
                else:
                    print(line)
        app_name = os.path.basename(file).replace('.apk.md', '')
        folder = file.split('/')[-2]
        entity = ner_dict[app_name]
        js = {"app_name": app_name, "folder": folder, "flaw_num": len(flaws), "flaws": flaws, "IOT_PRODUCT":entity["IOT_PRODUCT"],
              "PROTOCOL": entity["PROTOCOL"]}
        print(json.dumps(js), file=des)

if __name__ == '__main__':
    main()
    # load_ner_results()