#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2016/11/29 16:43
# @Author  : Shen Shi
# @Site    : 
# @File    : json2csv.py
# @Software: PyCharm Community Edition

'''
convert JSON format to CSV format
test
'''

import pandas as pd


def json2csv(json_path, json_file, csv_path=None, csv_file=None):
    if csv_path is None:
        csv_path = json_path
    if csv_file is None:
        csv_file = json_file.split(',')[0] + '.csv'

    file_handler = open(json_path.decode('utf-8') + json_file, "r")
    lines = file_handler.readlines()
    file_handler.close()
    content_list = []
    for line in lines:
        content_list.append(eval(line))

    df = pd.DataFrame(content_list)
    df.to_csv(csv_path.decode('utf-8') + csv_file)


if __name__ == '__main__':
    jsonpath = r"E:/BNU/我的师大云盘/数据/Twitter/Twitter-Haiyan/data/"
    jsonfile='haiyan.json'
    csvpath=jsonpath
    csvfile='haiyan.csv'
    json2csv(jsonpath, jsonfile, csvpath, csvfile)
