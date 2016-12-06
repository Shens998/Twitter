#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/6 9:48
# @Author  : Shen Shi
# @Site    : 
# @File    : SentimentAnalysis.py
# @Software: PyCharm Community Edition
import nltk

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print(tokens)

test