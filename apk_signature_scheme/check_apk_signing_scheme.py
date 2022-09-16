#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""
import os.path
import os

result_dir = "" # set path to the apksigner parsing result


def local_parse(apk_path, pkg_name):    
    """
    parse apk with apksigner
    :param apk_path: path to apk file
    :param pkg_name: package name of the app
    """
    result_path = f"{result_dir}/{pkg_name}.txt"
    if os.path.exists(apk_path):
        cmd = f"apksigner verify --print-certs --verbose  -Werr {apk_path} | tee {result_path}"
        os.system(cmd)
        print(f"\t[*] Analyzed: {pkg_name}")
    else:
        print(f"\t[-] No exist: {pkg_name}")


def parse_one_app(result_path):
    """
    parse one app's apksigner result
    :param result_path: path to the apksigner result

    :return: json object of the scheme result
    """
    res = ['', '', '', '']
    with open(result_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if "(JAR signing): " in line:
                line = line.split('(JAR signing): ')
                res[0] = line[1]
            elif "(APK Signature Scheme v2): " in line:
                line = line.split("(APK Signature Scheme v2): ")
                res[1] = line[1]
            elif "(APK Signature Scheme v3): " in line:
                line = line.split("(APK Signature Scheme v3): ")
                res[2] = line[1]
            elif "(APK Signature Scheme v4): " in line:
                line = line.split("(APK Signature Scheme v4): ")
                res[3] = line[1]
    result = []
    for r in res:
        if r == 'true':
            result.append(1)
        elif r == 'false':
            result.append(0)
        else:
            result.append(0)

    apk_signing_scheme = {
        "v1": result[0],
        "v2": result[1],
        "v3": result[2],
        "v4": result[3]
    }
    return apk_signing_scheme