#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: execution.py
@time: 3/25/20 12:15 PM
@description: this is for command line execution
"""

import subprocess
import logging
import traceback


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

