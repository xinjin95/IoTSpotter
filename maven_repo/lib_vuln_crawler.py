#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""

import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from urllib.error import URLError
import time

cooldown = 0.1
date_log_path = "data/maven_crawling/vulnerability.txt"
start_link_path = "data/maven_crawling/maven_matched.txt"
finished_link_path = "data/maven_crawling/lib_vul_finished.txt"
lib_file_path = "data/maven_crawling/lib_vul_sub_links.txt"

finished = set()
start_urls = set()
url_dir_map = dict()

def log_date(url, date_str):
    with open(date_log_path, 'a+') as f:
        print(json.dumps({"url": url, "vulnerability": date_str}), file=f)

def log_lib_file(url, sub_link):
    with open(lib_file_path, 'a+') as f:
        print(json.dumps({"url": url, "sub_link": sub_link}), file=f)

def is_target_file(link):
    if link.endswith('.aar') or link.endswith('.jar') or link.endswith('.pom'):
        return True
    else:
        return False

def extract_page_links(url, deepth):
    """
    Extracts all the links in a web page.
    :param url: url of the library maven repo page that may include vulnerability information
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
        print('\t', "[*] got response")
        # page_content = urlopen(req).read()
        soup = BeautifulSoup(page_content, 'html.parser')
        # urls = soup.find_all('a', href=True)
        trs = soup.find_all('tr')
        for tr in trs:
            if "Vulnerabilities" in str(tr):
                print("Vulnerability found:")
                target = tr.contents[1]
                links = target.find_all('a', href=True)
                links = [link['href'] for link in links]
                link = ' '.join(links)
                print('\n', link)
                log_date(url, link)
        res = soup.find_all('a', href=True)
        if res is not None:
            for link in res:
                link = urljoin(url, link['href'])
                if is_target_file(link):
                    log_lib_file(url, link)
        return

    except (URLError, UnicodeEncodeError) as e:

        print("Cannot explore this path: %s" % url)
        print(e)
        if deepth > 50:
            return
        time.sleep(cooldown)
        print('\t', "[-] try again")
        extract_page_links(url, deepth=deepth+1)


def get_start_links():
    with open(start_link_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            pkg_name = js["package_name"]
            matched_links = js["matched_links"]
            for link in matched_links:
                if link not in finished:
                    start_urls.add(link)
                    url_dir_map[link] = "./maven/" + pkg_name + '/'
    print("[#] Total # of start links:", len(start_urls))

def main():
    finished = get_finished()
    get_start_links()
    links = list(start_urls) 
    for i, link in enumerate(links):
        print(i, link)
        if link in finished:
            print("[*] finished on", link)
            continue
        extract_page_links(link, deepth=1)
        with open(finished_link_path, 'a+') as f:
            print(link, file=f)
        time.sleep(cooldown)

def record_finished():
    with open(finished_link_path, 'w+') as des:
        with open(date_log_path, 'r') as f:
            for line in f:
                js = json.loads(line)
                print(js["url"], file=des)

def get_finished():
    finished = set()
    with open(finished_link_path, 'r') as des:
        for line in des:
            line = line.strip('\n')
            finished.add(line)
    print("[*] finished:", len(finished))
    return finished

if __name__ == '__main__':
    main()