#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: master.py
@time: 6/12/21 11:42 PM
@desc:
"""
import random, time, queue
from multiprocessing.managers import BaseManager
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import gc

msg_save_path = "data/2M_lib_log/master_pure_non_iot_log.csv"
app_csv_path = "data/pure_non_iot_sha256.csv"
thread_num = 40
executor = ThreadPoolExecutor(max_workers=thread_num)
lock = threading.Lock()
messages = []
finished_index = []

# 发送任务的队列:
task_queue = queue.Queue()
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass


def get_finished(csv_file_path):
    finished = []
    if not os.path.isfile(csv_file_path):
        return finished
    with open(csv_file_path, 'r') as src:
        for line in src:
            try:
                line = line.split(',')
                finished.append(line[1])
            except:
                print(line)
    return finished

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5100), authkey=b'abc')
# 启动Queue:

manager.start()


# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()


def get_msg(task_id):
    try:
        print("start to receive:", task_id)
        msg = result.get(timeout=2000)
        print(task_id, "complete receiving:", msg)
        finished_index.append(task_id)
        # messages.append(msg)
    except:
        print("Timeout exception:", task_id)
        msg = "0,{},timeout".format(task_id)
        finished_index.append(task_id)
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
    # for pkg in app_removal:
    #     apk_path = "%s/%s.apk" % (package_dir, pkg)
    #     if os.path.isfile(apk_path):
    #         print("[-] finish removal:", pkg)
    #         os.remove(apk_path)


finished_apps = get_finished(msg_save_path)
finished_apps = set(finished_apps)
clear_finished_apks(finished_apps) # commented for test

print("finished on {} apps".format(len(finished_apps)))

# 放几个任务进去:
print('Put tasks...')

df = pd.read_csv(app_csv_path)
for index, pkg_name in enumerate(df['pkg_name']):
    # if index > 100: # set up for test
    #     continue
    if pkg_name in finished_apps:
        print("[*] finished", index, pkg_name)
        finished_index.append(index)
    else:
        task.put(str(index) + "," + pkg_name + "," + df["sha256"][index])

print("There are totally {} tasks".format(task.qsize()))
print('Try to get lib_results...')

del finished_apps
gc.collect()

# while True:
for i in range(len(df)):
    # if i in finished_index:
    #     print("[-] Have received:", i)
    #     continue
    executor.submit(get_msg, i)
    while executor._work_queue.qsize() > thread_num:
        print("Wait. Current:", executor._work_queue.qsize())
        time.sleep(1)

executor.shutdown(wait=True)

with open(msg_save_path, 'a+') as file:
    for msg in messages:
        print(msg, file=file)


manager.shutdown()
print('master exit.')