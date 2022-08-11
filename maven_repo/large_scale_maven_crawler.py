#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: large_scale_maven_crawler.py
@time: 8/5/21 3:20 PM
@desc:
"""
import json
import os.path

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
from os.path import split, exists, join, isfile
from collections import deque
import time

finished_log_path = "data/maven_crawling/large_scale_maven_finished.txt"
start_file_path = "data/maven_crawling/maven_matched.txt"
finished = set()
start_urls = set()
queue_file = "data/maven_crawling/q_items.txt"
cooldown = 3
url_dir_map = dict()
suffix = ["#maven", "#gradle", "#gradle-short", "#gradle-short-kotlin",
          "#sbt", "#ivy", "#grape", "#leiningen", "#buildr", "/usages",
          "?sort=newest", "?repo=jcenter"]


def get_finished():
    if os.path.exists(finished_log_path):
        with open(finished_log_path, 'r') as f:
            for line in f:
                line = line.strip('\n')
                finished.add(line)


def get_start_links():
    with open(start_file_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["package_name"]
            matched_links = js["matched_links"]
            for link in matched_links:
                if link not in finished:
                    start_urls.add(link)
                    url_dir_map[link] = "./maven/" + pkg_name + '/'
    print("[#] Total # of start links:", len(start_urls))


def init():
    get_finished()
    get_start_links()


def save_queue(items, file_path):
    with open(file_path, 'a+') as f:
        for item in items:
            print(item, file=f)


def download_file(url, save_dir):
    file_name = os.path.basename(url)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = save_dir + file_name
    if exists(file_path):
        print("\t[-] file already:", file_name)
    else:
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("\t[*] Successfully download:", file_name)


def extract_lib_files(url, save_dir, query_limit=-1):
    if url in finished:
        return
    print("[#] Visit url:", url)
    links_list = get_sub_links(url)
    q = deque(links_list)
    save_queue(links_list, queue_file)
    print("\t[*] Query and get {} sub-links".format(len(links_list)))
    num_lib_ext = 0
    limit_condition = lambda: num_lib_ext < query_limit if query_limit > 0 else lambda: True
    while len(q) != 0 and limit_condition():
        u = q.popleft()
        if u in finished:
            continue
        if not is_target_file(u):
            print("[#] Visit url:", u)
            time.sleep(cooldown)
            links_list = get_sub_links(u)
            print("\t[*] Query and get {} sub-links".format(len(links_list)))
            save_queue(links_list, queue_file)
            for link in links_list:
                if link in finished:
                    continue
                q.appendleft(link)
        else:
            log_finish(u)
            print("[#] Download target file:", u)
            download_file(u, save_dir=save_dir)



def log_finish(url):
    finished.add(url)
    with open(finished_log_path, 'a+') as f:
        print(url, file=f)


def get_sub_links(url):
    res = extract_page_links(url)
    log_finish(url)
    if res is None:
        print("\t[-] No sub_links for url:", url)
        return []
    else:
        sub_links = []
        for link in res:
            link = urljoin(url, link['href'])
            if "?p=" in url:
                tmp = url.split("?p=")
                # url = tmp[0]
                print("\t[#] Page number, mutate from {} to {}".format(url, tmp[0]))
                url = tmp[0]
            if "?repo=" in url:
                tmp = url.split("?repo=")
                print("\t[#] Page number, mutate from {} to {}".format(url, tmp[0]))
                url = tmp[0]
            if link not in finished and str(link).startswith(url) and not is_target_suffix(link):
                print("\t[*] Sub-link:", link)
                sub_links.append(link)
            elif is_target_file(link):
                print("\t[*] Target file:", link)
                sub_links.append(link)
            elif link in finished:
                print("\t[-] Finished on:", link)
            elif not str(link).startswith(url):
                print("\t[-] Not our target:", link)
        return sub_links


def is_target_suffix(link):
    for s in suffix:
        if link.endswith(s):
            print("\t\t[-] Target suffix:", link)
            return True
    return False


def is_target_file(link):
    if link.endswith('.aar') or link.endswith('.jar') or link.endswith('.pom'):
        return True
    else:
        return False


def extract_page_links(url):
    """
    Extracts all the links in a web page.
    :param url:
    :return:
    """

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    try:
        req = Request(url=url, headers=header)
        resp = urlopen(req)
        page_content = resp.read()
        # page_content = urlopen(req).read()
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup.find_all('a', href=True)

    except (URLError, UnicodeEncodeError) as e:

        print("Cannot explore this path: %s" % url)
        print(e)
        return None


def main():
    init()
    print(start_urls)
    for url in start_urls:
        extract_lib_files(url, url_dir_map[url])


def download_test():
    download_file("https://jcenter.bintray.com/com/inuker/bluetooth/library/1.3.9/library-1.3.9.aar", "maven/com.inuker.bluetooth/")


if __name__ == '__main__':
    # download_test()
    main()