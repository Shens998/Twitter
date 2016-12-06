#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/5 15:22
# @Author  : Shen Shi
# @Site    : 
# @File    : NetworkAnalysis.py
# @Software: PyCharm Community Edition

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

nodes = np.genfromtxt(".\data\haiyan-nodes.csv", dtype=str, delimiter=';', skip_header=1, usecols=(1))
links = np.genfromtxt(".\data\haiyan-links.csv", dtype=str, delimiter=';', skip_header=1, usecols=(0, 1))
Dg = nx.DiGraph()
Dg.add_nodes_from(nodes)
Dg.add_edges_from(links)
# 图太大会超过范围
# pos = nx.spring_layout(Dg)
degree = nx.degree_histogram(Dg)
xAix = range(len(degree))
yAix = [z/float(sum(degree))for z in degree]

print(degree)
plt.figure(1)
plt.loglog(xAix, yAix, color="blue", linewidth=2)
plt.figure(2)
# nx.draw_network_edges(Dg, pos)
# nx.draw_network_nodes(Dg, pos)
degree_sequence = sorted(nx.degree(Dg).values(), reverse=True)
plt.loglog(degree_sequence)
plt.figure(3)
plt.bar(xAix, degree, width=1.8)
plt.show()
