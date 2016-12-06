#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/5 11:18
# @Author  : Shen Shi
# @Site    : 
# @File    : StatisticAnalysis.py
# @Software: PyCharm Community Edition

import numpy as np
import matplotlib.pyplot as plt

links = np.genfromtxt(".\data\haiyan-links.csv", dtype=str, delimiter=';', skip_header=1, usecols=(0,1))
dic = {}
for n in sorted(np.reshape(links, -1)):
    if n not in dic:
        dic[n] = 1
    else:
        dic[n] += 1
plt.bar(range(95), dic)
plt.xticks(range(95), dic, rotation=90)
plt.show()
