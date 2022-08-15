#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: check_scheme.py
@time: 1/19/22 6:13 PM
@desc:
"""
import os.path

import pandas as pd
import glob
import subprocess

# apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
apk_dir = "/home/xxx/Documents/project/iot_measurement/lib_update_apks/"
app_list_csv = "/home/xxx/Documents/code/python/iot-measure/data/androzoo/description-improvement/shared_37K_pkg_download_rank.csv"
result_dir = "/home/xxx/Documents/code/python/iot-measure/apk_signature_scheme/data/apksigner_results"

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

def get_finished():
    files = glob.glob(result_dir + '/*')
    res = set()
    for file in files:
        file = os.path.basename(file)[:-4]
        res.add(file)
    print(f"Finished: {len(res)}")
    with open("/home/xxx/Documents/code/python/iot-measure/apk_signature_scheme/data/finished_apps.txt", 'w') as f:
        for app in res:
            print(app, file=f)
    return res


def local_parse():
    finished = get_finished()
    df = pd.read_csv(app_list_csv)
    for i, pkg_name in enumerate(df['app_name']):
        print(i)
        apk_path = f'{apk_dir}{pkg_name}.apk'
        result_path = f"{result_dir}/{pkg_name}.txt"
        if pkg_name in finished:
            print(f"\t[+] Finished: {pkg_name}")
        elif os.path.exists(apk_path):
            cmd = f"apksigner verify --print-certs --verbose  -Werr {apk_path} | tee {result_path}"
            os.system(cmd)
            print(f"\t[*] Analyzed: {pkg_name}")
        else:
            print(f"\t[-] No exist: {pkg_name}")


def download_one_app(package_name):
    exe = Executor(work_path=apk_dir)
    cmd = f"wget -q http://164.107.119.61:8882/storage2/apks/xxxxxx.2021.04/{package_name}.apk"
    exe.execute(cmd)

def remote_parse():
    finished = get_finished()
    df = pd.read_csv(app_list_csv)
    failed_apps = []
    for i, pkg_name in enumerate(df['app_name']):
        print(i, pkg_name)
        if pkg_name in finished:
            print(f"\t[*] finished on {pkg_name}")
            continue
        download_one_app(pkg_name)
        apk_path = f'{apk_dir}{pkg_name}.apk'
        result_path = f"{result_dir}/{pkg_name}.txt"
        if os.path.exists(apk_path):
            print(f"\t[*] app successfully downloaded:", pkg_name)
            cmd = f"apksigner verify --print-certs --verbose  -Werr {apk_path} | tee {result_path}"
            os.system(cmd)
            print(f"\t[*] Analyzed: {pkg_name}")
            os.remove(apk_path)
            if not os.path.exists(apk_path):
                print(f"\t\t[*] removed:", pkg_name)
            else:
                print(f"\t\t[-] failed removing:", pkg_name)
        else:
            print(f"\t[-] No exist: {pkg_name}")


if __name__ == '__main__':
    # main() # 18:24, 110
    get_finished()
    # remote_parse()