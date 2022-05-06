#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: aggregate_cognicrypt.py
@time: 10/10/21 5:37 PM
@desc:
"""
import json
import pandas as pd

src_file = "cognicrypt_results/cognicrypt_flaws.txt"

def get_rule_names():
    rules = """javax.net.ssl.TrustManagerFactory
javax.crypto.Cipher
java.security.AlgorithmParameters
java.security.KeyPairGenerator
java.security.cert.TrustAnchor
java.security.spec.DSAParameterSpec
javax.crypto.SecretKey
javax.net.ssl.SSLParameters
Stopwatch
javax.net.ssl.SSLContext
javax.net.ssl.CertPathTrustManagerParameters
SSLSocketFactory
java.security.spec.DSAGenParameterSpec
javax.crypto.spec.DHGenParameterSpec
java.security.DigestOutputStream
javax.crypto.SecretKeyFactory
java.security.DigestInputStream
java.security.Key
javax.crypto.spec.DHParameterSpec
java.security.KeyPair
javax.net.ssl.KeyManagerFactory
java.security.KeyStore
com.amazonaws.services.kms.model.GenerateDataKeyRequest
javax.crypto.KeyGenerator
javax.crypto.Mac
SSLSocket
java.security.cert.PKIXBuilderParameters
SSLServerSocket
javax.net.ssl.KeyStoreBuilderParameters
javax.crypto.CipherOutputStream
java.security.SecureRandom
javax.crypto.spec.IvParameterSpec
java.security.spec.RSAKeyGenParameterSpec
javax.crypto.spec.SecretKeySpec
javax.crypto.spec.PBEParameterSpec
MessageDigest
javax.crypto.CipherInputStream
javax.net.ssl.SSLEngine
javax.crypto.spec.PBEKeySpec
SSLServerSocketFactory
javax.crypto.spec.GCMParameterSpec
javax.xml.crypto.dsig.spec.HMACParameterSpec
java.security.Signature
java.security.cert.PKIXParameters"""

    rules = rules.split('\n')
    print(rules)
    res = {}
    for rule in rules:
        res[rule] = []
    print(res)

def get_violation_per_apps():
    overall_rule = {'javax.net.ssl.TrustManagerFactory': [], 'javax.crypto.Cipher': [], 'java.security.AlgorithmParameters': [], 'java.security.KeyPairGenerator': [], 'java.security.cert.TrustAnchor': [], 'java.security.spec.DSAParameterSpec': [], 'javax.crypto.SecretKey': [], 'javax.net.ssl.SSLParameters': [], 'Stopwatch': [], 'javax.net.ssl.SSLContext': [], 'javax.net.ssl.CertPathTrustManagerParameters': [], 'SSLSocketFactory': [], 'java.security.spec.DSAGenParameterSpec': [], 'javax.crypto.spec.DHGenParameterSpec': [], 'java.security.DigestOutputStream': [], 'javax.crypto.SecretKeyFactory': [], 'java.security.DigestInputStream': [], 'java.security.Key': [], 'javax.crypto.spec.DHParameterSpec': [], 'java.security.KeyPair': [], 'javax.net.ssl.KeyManagerFactory': [], 'java.security.KeyStore': [], 'com.amazonaws.services.kms.model.GenerateDataKeyRequest': [], 'javax.crypto.KeyGenerator': [], 'javax.crypto.Mac': [], 'SSLSocket': [], 'java.security.cert.PKIXBuilderParameters': [], 'SSLServerSocket': [], 'javax.net.ssl.KeyStoreBuilderParameters': [], 'javax.crypto.CipherOutputStream': [], 'java.security.SecureRandom': [], 'javax.crypto.spec.IvParameterSpec': [], 'java.security.spec.RSAKeyGenParameterSpec': [], 'javax.crypto.spec.SecretKeySpec': [], 'javax.crypto.spec.PBEParameterSpec': [], 'MessageDigest': [], 'javax.crypto.CipherInputStream': [], 'javax.net.ssl.SSLEngine': [], 'javax.crypto.spec.PBEKeySpec': [], 'SSLServerSocketFactory': [], 'javax.crypto.spec.GCMParameterSpec': [], 'javax.xml.crypto.dsig.spec.HMACParameterSpec': [], 'java.security.Signature': [], 'java.security.cert.PKIXParameters': []}
    apps = []
    total_flaws = []
    # rules = set()
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            rule_dict = {'javax.net.ssl.TrustManagerFactory': 0, 'javax.crypto.Cipher': 0, 'java.security.AlgorithmParameters': 0, 'java.security.KeyPairGenerator': 0, 'java.security.cert.TrustAnchor': 0, 'java.security.spec.DSAParameterSpec': 0, 'javax.crypto.SecretKey': 0, 'javax.net.ssl.SSLParameters': 0, 'Stopwatch': 0, 'javax.net.ssl.SSLContext': 0, 'javax.net.ssl.CertPathTrustManagerParameters': 0, 'SSLSocketFactory': 0, 'java.security.spec.DSAGenParameterSpec': 0, 'javax.crypto.spec.DHGenParameterSpec': 0, 'java.security.DigestOutputStream': 0, 'javax.crypto.SecretKeyFactory': 0, 'java.security.DigestInputStream': 0, 'java.security.Key': 0, 'javax.crypto.spec.DHParameterSpec': 0, 'java.security.KeyPair': 0, 'javax.net.ssl.KeyManagerFactory': 0, 'java.security.KeyStore': 0, 'com.amazonaws.services.kms.model.GenerateDataKeyRequest': 0, 'javax.crypto.KeyGenerator': 0, 'javax.crypto.Mac': 0, 'SSLSocket': 0, 'java.security.cert.PKIXBuilderParameters': 0, 'SSLServerSocket': 0, 'javax.net.ssl.KeyStoreBuilderParameters': 0, 'javax.crypto.CipherOutputStream': 0, 'java.security.SecureRandom': 0, 'javax.crypto.spec.IvParameterSpec': 0, 'java.security.spec.RSAKeyGenParameterSpec': 0, 'javax.crypto.spec.SecretKeySpec': 0, 'javax.crypto.spec.PBEParameterSpec': 0, 'MessageDigest': 0, 'javax.crypto.CipherInputStream': 0, 'javax.net.ssl.SSLEngine': 0, 'javax.crypto.spec.PBEKeySpec': 0, 'SSLServerSocketFactory': 0, 'javax.crypto.spec.GCMParameterSpec': 0, 'javax.xml.crypto.dsig.spec.HMACParameterSpec': 0, 'java.security.Signature': 0, 'java.security.cert.PKIXParameters': 0}
            flaws = js["flaws"]
            flaw_num = js["flaw_num"]
            for flaw in flaws:
                rule = flaw["rule_name"]
                rule_dict[rule] += 1
            apps.append(app_name)
            total_flaws.append(flaw_num)
            for rule, value in rule_dict.items():
                overall_rule[rule].append(value)
    res = {"app_name": apps}
    for key, val in overall_rule.items():
        res[key] = val
    res["total_flaw_num"] = total_flaws
    df = pd.DataFrame(res)
    df = df.sort_values("total_flaw_num", ascending=False)
    df.to_csv("cognicrypt_results/accumulated_result_for_app.csv", index=False)


def get_empty_rule_dict():
    res = dict()
    for i in ['ConstraintError', 'IncompleteOperationError', 'TypestateError',
              'ImpreciseValueExtractionError', 'RequiredPredicateError', 'ForbiddenMethodError']:
        res[str(i)] = []
    print(res)
    return res


def get_package_name_from_class(class_name):
    # print(method)
    try:
        tmp = class_name.split('.')
        if len(tmp[:-1]) < 1:
            return None
        package_name = '.'.join(tmp[:-1])
        return package_name
    except:
        print(class_name)
        return None

def get_violation_per_lib():
    overall_rule = dict()
    libs = []
    rule_dict = dict()
    with open(src_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            app_name = js["app_name"]
            # flaws = js["flaws"]
            # flaw_num = js["flaw_num"]
            flaws = js["flaws"]
            flaw_num = js["flaw_num"]
            for flaw in flaws:
                rule = flaw["rule_name"]
                if "class" not in flaw:
                    continue
                className = flaw["class"]
                package_name = get_package_name_from_class(className)
                if package_name is None or package_name.startswith(app_name):
                    continue
                # rule_dict =
                if package_name not in overall_rule:
                    overall_rule[package_name] = {'javax.net.ssl.TrustManagerFactory': 0, 'javax.crypto.Cipher': 0, 'java.security.AlgorithmParameters': 0, 'java.security.KeyPairGenerator': 0, 'java.security.cert.TrustAnchor': 0, 'java.security.spec.DSAParameterSpec': 0, 'javax.crypto.SecretKey': 0, 'javax.net.ssl.SSLParameters': 0, 'Stopwatch': 0, 'javax.net.ssl.SSLContext': 0, 'javax.net.ssl.CertPathTrustManagerParameters': 0, 'SSLSocketFactory': 0, 'java.security.spec.DSAGenParameterSpec': 0, 'javax.crypto.spec.DHGenParameterSpec': 0, 'java.security.DigestOutputStream': 0, 'javax.crypto.SecretKeyFactory': 0, 'java.security.DigestInputStream': 0, 'java.security.Key': 0, 'javax.crypto.spec.DHParameterSpec': 0, 'java.security.KeyPair': 0, 'javax.net.ssl.KeyManagerFactory': 0, 'java.security.KeyStore': 0, 'com.amazonaws.services.kms.model.GenerateDataKeyRequest': 0, 'javax.crypto.KeyGenerator': 0, 'javax.crypto.Mac': 0, 'SSLSocket': 0, 'java.security.cert.PKIXBuilderParameters': 0, 'SSLServerSocket': 0, 'javax.net.ssl.KeyStoreBuilderParameters': 0, 'javax.crypto.CipherOutputStream': 0, 'java.security.SecureRandom': 0, 'javax.crypto.spec.IvParameterSpec': 0, 'java.security.spec.RSAKeyGenParameterSpec': 0, 'javax.crypto.spec.SecretKeySpec': 0, 'javax.crypto.spec.PBEParameterSpec': 0, 'MessageDigest': 0, 'javax.crypto.CipherInputStream': 0, 'javax.net.ssl.SSLEngine': 0, 'javax.crypto.spec.PBEKeySpec': 0, 'SSLServerSocketFactory': 0, 'javax.crypto.spec.GCMParameterSpec': 0, 'javax.xml.crypto.dsig.spec.HMACParameterSpec': 0, 'java.security.Signature': 0, 'java.security.cert.PKIXParameters': 0}
                overall_rule[package_name][rule] = overall_rule[package_name][rule] + 1
                # overall_rule[package_name] =
    total_flaws = []
    for lib, value in overall_rule.items():
        libs.append(lib)
        total = 0
        for k, v in value.items():
            if k not in rule_dict:
                rule_dict[k] = []
            rule_dict[k].append(v)
            total += v
        total_flaws.append(total)

    # libs = []
    # rule_all = dict()

    res = {"3rd_party_lib": libs}
    for key, val in rule_dict.items():
        res["rule_"+key] = val
    res["total_flaw_num"] = total_flaws
    df = pd.DataFrame(res)
    df = df.sort_values("total_flaw_num", ascending=False)
    df.to_csv("cognicrypt_results/accumulated_result_for_lib.csv", index=False)

def get_most_popular_rule():
    df = pd.read_csv("cognicrypt_results/accumulated_result_for_app.csv")
    df = df.loc[df["ConstraintError"] > 0]
    print(len(df))


def get_apps_with_at_lease_one_violations():
    df = pd.read_csv("cognicrypt_results/accumulated_result_for_app.csv")
    df = df.loc[df["total_flaw_num"] > 0]
    print(len(df))


def get_app_num_per_rule():
    df = pd.read_csv("cognicrypt_results/accumulated_result_for_app.csv")
    app_num = []
    for col_name in ['javax.net.ssl.TrustManagerFactory', 'javax.crypto.Cipher', 'java.security.AlgorithmParameters', 'java.security.KeyPairGenerator', 'java.security.cert.TrustAnchor', 'java.security.spec.DSAParameterSpec', 'javax.crypto.SecretKey', 'javax.net.ssl.SSLParameters', 'Stopwatch', 'javax.net.ssl.SSLContext', 'javax.net.ssl.CertPathTrustManagerParameters', 'SSLSocketFactory', 'java.security.spec.DSAGenParameterSpec', 'javax.crypto.spec.DHGenParameterSpec', 'java.security.DigestOutputStream', 'javax.crypto.SecretKeyFactory', 'java.security.DigestInputStream', 'java.security.Key', 'javax.crypto.spec.DHParameterSpec', 'java.security.KeyPair', 'javax.net.ssl.KeyManagerFactory', 'java.security.KeyStore', 'com.amazonaws.services.kms.model.GenerateDataKeyRequest', 'javax.crypto.KeyGenerator', 'javax.crypto.Mac', 'SSLSocket', 'java.security.cert.PKIXBuilderParameters', 'SSLServerSocket', 'javax.net.ssl.KeyStoreBuilderParameters', 'javax.crypto.CipherOutputStream', 'java.security.SecureRandom', 'javax.crypto.spec.IvParameterSpec', 'java.security.spec.RSAKeyGenParameterSpec', 'javax.crypto.spec.SecretKeySpec', 'javax.crypto.spec.PBEParameterSpec', 'MessageDigest', 'javax.crypto.CipherInputStream', 'javax.net.ssl.SSLEngine', 'javax.crypto.spec.PBEKeySpec', 'SSLServerSocketFactory', 'javax.crypto.spec.GCMParameterSpec', 'javax.xml.crypto.dsig.spec.HMACParameterSpec', 'java.security.Signature', 'java.security.cert.PKIXParameters']:
        # col_name = 'rule_{}'.format(i)
        tmp = df.loc[df[col_name] > 0]
        app_num.append(str(len(tmp)))
    with open('cognicrypt_results/rule_num_apps.csv', 'a+') as f:
        print(','.join(app_num), file=f)

# get_violation_per_apps()
# get_empty_rule_dict()
# get_violation_per_lib()
# get_most_popular_rule()
# get_apps_with_at_lease_one_violations()
# get_app_num_per_rule()
# get_rule_names()
get_app_num_per_rule()