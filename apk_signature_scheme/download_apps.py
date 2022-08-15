#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: download_apps.py
@time: 1/20/22 10:30 AM
@desc:
"""
from hashlib import sha256
import _thread
# import pandas as pd
import os
import subprocess
import time

apk_dir = "/apks/apks/xxxxxx.2021.04"
csv_path = "xxx_xxx_shared_sha256_androzoo.csv"

num_threads = 20
thread_ids = list(range(num_threads))
packages_failed = []
package_succeed = []
download_finished = set()

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

def download_one_package(package_name, sha, thread_id):
    pkg = package_name
    if check_sha(pkg, sha):
        thread_ids.append(thread_id)
        print(f"[*] {pkg} has been downloaded")
        return
    else:
        print("[-] sha256 mismatch:", pkg)
        if os.path.exists("%s/%s.apk" % (apk_dir, pkg)):
            print(f"[-] remove old app:", pkg)
            os.remove("%s/%s.apk" % (apk_dir, pkg))
    package_dir = apk_dir
    exe = Executor(work_path=package_dir)
    print("thread: %d for %s" % (thread_id, package_name))
    # cmd = "curl --silent -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
    #       " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
    cmd = "curl -O --remote-header-name -G -d apikey=cbd81226806588c5be781727bdbec483890f514bf2f0981721dc124869cf9404" \
          " -d sha256=%s https://androzoo.uni.lu/api/download" % sha
    exe.execute(cmd)
    if not os.path.exists("%s/%s.apk" % (package_dir, sha)):
        packages_failed.append(package_name)
        thread_ids.append(thread_id)
        return
    with open("%s/%s.apk" % (package_dir, sha), 'rb') as file:
        data = file.read()
        sha256_returned = sha256(data).hexdigest()
        if sha256_returned.lower() == str(sha).lower():
            cmd = "mv %s.apk %s.apk" % (sha, package_name)
            print("[*] sha256 matches:", package_name)
            exe.execute(cmd)
            package_succeed.append(package_name)
        else:
            cmd = "rm %s.apk" % sha
            exe.execute(cmd)
            print("[-] sha256 matches:", package_name)
            packages_failed.append(package_name)
    thread_ids.append(thread_id)

def check_sha(apk_name, sha):
    package_dir = apk_dir
    if not os.path.exists("%s/%s.apk" % (package_dir, apk_name)):
        return False
    with open("%s/%s.apk" % (package_dir, apk_name), 'rb') as file:
        data = file.read()
        sha256_returned = sha256(data).hexdigest()
        return sha256_returned.lower() == str(sha).lower()

def clear_finished_apks(app_csv_path):
    package_dir = apk_dir + '/'
    # dataFrame = pd.read_csv(app_csv_path)
    pkgs = []
    shas = []
    with open(app_csv_path, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            # time.sleep(1)
            line = line.split(',')
            pkg = line[0]
            sha = line[1]
            print(i, pkg, sha)
            pkgs.append(pkg)
            shas.append(sha)
            # if check_sha(pkg, sha):
            #     download_finished.add(pkg)
            # else:
            #     print("[-] sha256 mismatch:", pkg)
            #     if os.path.exists("%s%s.apk" % (package_dir, pkg)):
            #         os.remove("%s%s.apk" % (package_dir, pkg))
    print(f"{len(download_finished)} apps have been downloaded")
    time.sleep(3)

    return {"pkg_name": pkgs, "sha256": shas}
    # for k, pkg in enumerate(dataFrame['pkg_name']):
    #     if os.path.exists("%s%s.apk" % (package_dir, pkg)):
    #         sha = dataFrame["sha256"][k]
    # _, _, filenames = next(os.walk(package_dir))
    # print("Remove:", len(filenames) - len(download_finished))
    # for file_name in filenames:
    #     if file_name.endswith(".apk"):
    #         app_name = file_name.replace(".apk", '')
    #         if app_name not in download_finished:
    #             apk_path = "%s%s.apk" % (package_dir, app_name)
    #             if not os.path.isfile(apk_path):
    #                 print(apk_path, "not exist!")
    #                 continue
    #             os.remove(apk_path)
    #             print("[-] incomplete download removal:", app_name)

def main():
    df = clear_finished_apks(csv_path)
    packages = df["pkg_name"]
    shas = df["sha256"]
    for i, package in enumerate(packages):
        # if package in download_finished:
        #     print(f"[-] {i}-th finished:", package)
        #     continue
        print("download %d-th app: %s" % (i, package))
        while len(thread_ids) == 0:
            time.sleep(0.1)
        _thread.start_new_thread(download_one_package, (package, shas[i], thread_ids.pop()))

    while num_threads != len(thread_ids):
        time.sleep(1)
    with open("failed.txt", 'w+') as f:
        for app in packages_failed:
            print(app, file=f)

def handle_failed():
    df = clear_finished_apks(csv_path)
    packages = df["pkg_name"]
    shas = df["sha256"]
    failed = set()
    with open('failed.txt', 'r') as f:
        for line in f:
            line = line.strip('\n')
            failed.add(line)
    for i, pkg_name in enumerate(packages):
        if pkg_name in failed:
            sha = shas[i]
            download_one_package(pkg_name, sha, 0)

# main()
# clear_finished_apks(csv_path)
handle_failed()