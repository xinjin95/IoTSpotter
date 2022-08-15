#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: crypto_validation.py
@time: 1/14/22 7:10 PM
@desc:
"""
import json
import os.path
import subprocess
import pandas as pd

selected_apks = ['com.tiqiaa.remote', 'vstc.vscam.client', 'push.lite.avtech.com', 'com.remotefairy4',
                'com.specialyg.ippro', 'com.tekoia.sure.activities', 'wifi.control.samsung', 'wifi.control.lg',
                'com.realme.link', 'com.xiaomi.router', 'com.google.vr.vrcore', 'com.samsung.android.oneconnect',
                'com.dsi.ant.plugins.antplus', 'com.google.android.apps.chromecast.app', 'com.sec.app.samsungprintservice',
                'com.sonyericsson.extras.liveware', 'com.dsi.ant.service.socket', 'com.sec.android.app.shealth',
                'com.samsung.android.app.watchmanager', 'com.hp.android.printservice']

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

def check_existence():
    apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
    for app in selected_apks:
        apk_path = apk_dir + app + '.apk'
        if not os.path.exists(apk_path):
            print(app)


def main():
    # file_path = "/home/xxx/Documents/code/python/iot-measure/crypto_analysis/data/call_graph_analysis/iot_lib_apps.txt"
    # jar_path = "callGraphAnalzer.jar"
    jar_path = "cryptoValidation.jar"
    apk_dir = "/home/xxx/Documents/project/iot_measurement/iot_lib_apps/"
    exe = Executor(work_path="/home/xxx/Documents/code/python/iot-measure/crypto_analysis/data/call_graph_analysis/")
    # with open(file_path, 'r') as f:
    for i, pkg_name in enumerate(selected_apks):
        # if i < 94: # com.lgeha.nuts
        #     continue
        # pkg_name = line.strip('\n')
        cmd = "java -jar {} {}{}.apk".format(jar_path, apk_dir, pkg_name)
        # print(cmd)
        exe.execute(cmd)

def split_result():
    files = ["data/call_graph_analysis/cryptoguard/cryptoguard_call_analysis.txt",
             "data/call_graph_analysis/cognitive/cognicrypt_call_analysis.txt"]
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                js = json.loads(line)
                del js['IOT_PRODUCT']
                pkg_name = js['app_name']
                if 'cryptoguard' in file:
                    with open(f"data/call_graph_analysis/xxx_validation/cryptoguard/{pkg_name}.json", 'w+') as des:
                        json.dump(js, des)
                else:
                    with open(f"data/call_graph_analysis/xxx_validation/cognicrypt/{pkg_name}.json", 'w+') as des:
                        json.dump(js, des)

if __name__ == '__main__':
    # check_existence()
    # main()
    split_result()