#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: check_availability_gplay.py
@time: 1/14/21 9:20 PM
@desc:
"""
from iot_app_collector.crawler import get_package_list, record_result
from aiohttp import web
import asyncio
from aiohttp import ClientSession
import pandas as pd
import socket
import aiohttp
import time
import async_timeout


str_no_found = "the requested URL was not found on this server"
res = []


async def fetch(package, session):
    url = "https://play.google.com/store/apps/details?id={}"
    req = url.format(package)
    print(req)
    with async_timeout.timeout(300):
        async with session.get(req) as response:
            res.append("%s,%d" % (package, response.status))
            print("%s,%d" % (package, response.status))


async def run(packages):
    tasks = []
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )
    async with ClientSession(connector=conn) as session:
        for package in packages:
            # print(url.format(package))
            task = asyncio.ensure_future(fetch(package, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

def main():
    file_path = "../data/package/iot_package_seeds.txt"
    apps = get_package_list(file_path)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(apps))
    loop.run_until_complete(future)
    result_path = "../data/package/availability_check_result.csv"
    record_result(result_path, res, is_dict=False)


def get_available_apps():
    path_response_code_result = "../data/package/availability_check_result.csv"
    df = pd.read_csv(path_response_code_result)
    available_packages = []
    for i, package in enumerate(df["package_name"]):
        rep_code = df["response_code"][i]
        if rep_code == 200:
            available_packages.append(package)
    path_available_apps = "../data/package/iot_package_available.txt"
    record_result(path_available_apps, available_packages)


if __name__ == '__main__':
    get_available_apps()