#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""
from bs4 import BeautifulSoup as bs
import requests
import csv
import time
import random
import json
import os
import pandas as pd

target_package_path = "data/3rd_party_lib/filtered_package_names.txt" # path to the list of library package names
# finished_path = "../data/google_search/finished.txt"
result_path = "data/google_search/search_for_maven.txt"
package_list = list()


def extract_links(search_term,number_results=15):
    '''
    Returns a list of top 15 links from google search results
    '''
    headers={
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0"
    }

    def link_parser(raw_html):
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for num,result in enumerate(result_block):
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                yield link['href']

    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}'.format(escaped_search_term,number_results+1)
    response = requests.get(google_url, headers=headers)
    print(f'\tResponse code: {response.status_code}')
    while response.status_code == 429:
        print(f'Invalid response code, sleep for 120s')
        time.sleep(120)
        response = requests.get(google_url, headers=headers)
        print(f'\tResponse code: {response.status_code}')
    soup = bs(response.text, 'html.parser')
    return list(link_parser(soup))


def get_link_root(url):
    try:
        url=url.split('://')[1].replace('www.','').split('.')[0]
        return url
    except:
        try:
            url=url.replace('www.','').split('.')[0]
            return url
        except:
            return url


def get_new_randomnumber(previous):
    randomnumber=random.randint(5,15)
    # print('\titer:',randomnumber)
    if randomnumber==previous:
        return get_new_randomnumber(randomnumber)
    else:
        return randomnumber

def get_package_list():
    with open(target_package_path, 'r') as f:
        for line in f:
            package_list.append(line.strip())
    return package_list

def main():
    package_list = get_package_list()
    print(f"[*] # of packages: {len(package_list)}")
    previous_pause = 0
    for i, pkg_name in enumerate(package_list):
        search_item = pkg_name + " maven"
        print(f"[-] Search: {search_item}")
        links = extract_links(search_item)
        print(f'\t# of links: {len(links)}')
        randomnumber = get_new_randomnumber(previous_pause)
        previous_pause = randomnumber
        print(f'\tSleeping {randomnumber}s..')
        time.sleep(randomnumber)
        js = {"package_name": pkg_name, "search_item": search_item, "links": links}
        with open("data/google_search/search_for_maven.txt", 'a+') as f:
            print(json.dumps(js), file=f)


def search_test():
    search_item = "com.videogo.common"
    res = extract_links(search_item)
    print(res)


def check_search_results():
    visited = set()
    with open("data/google_search/search_for_maven.txt", 'r') as f:
        for i, line in enumerate(f):
            js = json.loads(line)
            package_name = js["package_name"]
            if package_name in visited:
                print(i, package_name)
            visited.add(package_name)

def check_search_results():
    result_path = "data/google_search/search_for_maven.txt"
    visited = set()
    res_package_names = []
    res_links = []
    with open(result_path, 'r') as file:
        for line in file:
            js = json.loads(line)
            package_name = js["package_name"]
            search_item = js["search_item"]
            links = js["links"]
            # print(package_name)
            for link in links:
                if link.startswith("https://mvnrepository.com/artifact/"):
                    # print(package_name, link)
                    rest_part = link.replace("https://mvnrepository.com/artifact/", "")
                    if '/' in rest_part:
                        lib_name, _ = rest_part.split('/', 1)
                    else:
                        lib_name = rest_part
                        continue
                    if package_name.startswith(lib_name) or lib_name in package_name:
                        # print('\t', link)
                        parts = rest_part.split('/')
                        if len(parts) >= 3:
                            retain_part = parts[:2]
                            retain_part = '/'.join(retain_part)
                            link = "https://mvnrepository.com/artifact/" + retain_part
                            print(rest_part, retain_part)
                        if link not in visited:
                            res_package_names.append(package_name)
                            res_links.append(link)

                    # print(package_name, lib_name)
                    visited.add(link)

    df = pd.DataFrame({
        "package_name": res_package_names,
        "links": res_links,
    })
    df.to_csv("data/google_search/target_links.csv", index=False)

if __name__ == '__main__':
    main()