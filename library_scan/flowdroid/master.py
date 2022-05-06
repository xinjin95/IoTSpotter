#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: master.py
@time: 8/4/21 10:35 AM
@desc:
"""
import random, time, queue
from multiprocessing.managers import BaseManager
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import gc

msg_save_path = "data/master_log.csv"
target_app_path = "data/target_apps.txt"
flowdroid_result_dir = "data/analysis_results/"
app_csv_path = "data/target_sha.csv"

thread_num = 20
executor = ThreadPoolExecutor(max_workers=thread_num)
lock = threading.Lock()
messages = []
finished_apps = set()
finished_index = []

task_queue = queue.Queue()
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass


# def get_app_list() -> list:
#     result = list()
#     with open(target_app_path, 'r') as file:
#         for line in file:
#             app_name = line.strip('\n')
#             xml_path = flowdroid_result_dir + app_name + '.xml'
#             if os.path.exists(xml_path):
#                 print("[-] Finished on:", app_name)
#                 finished_apps.append(app_name)
#                 continue
#             result.append(app_name)
#     return result


def get_msg(task_id):
    try:
        print("start to receive:", task_id)
        msg = result.get(timeout=2000)
        print(task_id, "complete receiving:", msg)
        # messages.append(msg)
    except:
        print("Timeout exception:", task_id)
        msg = "0,{},timeout".format(task_id)
        # messages.append(msg)
    with lock:
        with open(msg_save_path, 'a+') as des:
            print(msg, file=des)


def clear_finished_apks(finished_pkgs):
    app_removal = set()
    dataFrame = pd.read_csv(app_csv_path)
    for k, pkg in enumerate(dataFrame['pkg_name']):
        if pkg in finished_pkgs:
            app_removal.add(pkg)
        app_removal.add(dataFrame['sha256'][k])
    print("Should remove {} apps' apk files".format(len(app_removal)))
    # package_dir = "/users/PAS1888/zyueinfosec/xinjin/third_party_library/data/apks/"
    package_dir = "data/apks/"
    _, _, filenames = next(os.walk(package_dir))
    for file_name in filenames:
        if file_name.endswith(".apk"):
            app_name = file_name.replace(".apk", '')
            if app_name in app_removal:
                apk_path = "%s%s.apk" % (package_dir, app_name)
                if not os.path.isfile(apk_path):
                    print(apk_path, "not exist!")
                    continue
                os.remove(apk_path)
                print("[-] finish removal:", app_name)


QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

manager = QueueManager(address=('', 7100), authkey=b'abc')
manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

print('Put tasks...')

df = pd.read_csv(app_csv_path)
for index, pkg_name in enumerate(df['pkg_name']):
    # if index > 100: # set up for test
    #     continue
    xml_path = flowdroid_result_dir + pkg_name + '.xml'
    if os.path.exists(xml_path):
        # print("[-] Finished on:", pkg_name)
        finished_apps.add(pkg_name)
    if pkg_name in finished_apps:
        print("[*] finished", index, pkg_name)
        finished_index.append(index)
    else:
        task.put(str(index) + "," + pkg_name + "," + df["sha256"][index])

print("finished on {} apps".format(len(finished_apps)))
clear_finished_apks(finished_apps)

del finished_apps
gc.collect()


for i in range(len(df)):
    # if i in finished_index:
    #     print("[-] Have received:", i)
    #     continue
    executor.submit(get_msg, i)
    while executor._work_queue.qsize() > thread_num:
        print("Wait. Current:", executor._work_queue.qsize())
        time.sleep(1)

executor.shutdown(wait=True)

manager.shutdown()
print('master exit.')