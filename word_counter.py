#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import collections

if __name__ == "__main__":
    
    # f = open("gutenburg.txt","r",encoding='UTF8')
    # content = f.read()
    # f.close()

    # words = re.split(' |-',content)

    # unwanted_chars = "-— .,_?!*1234567890[]\#:();"
    # wordfreq = {}
    # for raw_word in words:
    #     word = "".join([ c if c.isalpha() else "" for c in raw_word ]).lower()

    #     if word == "" :
    #         continue
        
    #     if word not in wordfreq:
    #         wordfreq[word] = 0
    #     wordfreq[word]+=1

    # f = open("word_count.txt","w",encoding='UTF8')

    # for key, value in wordfreq.items():
    #     f.write('%s:%s\n' % (key, value))

    # f.close()

    wordfreq = collections.Counter()
    unwanted_chars = "-— .,_?!*1234567890[]\#:();”“"
    with open("gutenburg.txt","r",encoding = "UTF8") as f:
        line_data = f.readline()
        while line_data:
            line = "".join([ c if c.isalpha() else " " for c in line_data ]).lower()
            wordfreq.update(line.split())
            line_data = f.readline()
    
    with open("word_count.txt","w",encoding = "UTF8") as f:
        for key, value in wordfreq.items():
            f.write('%s:%s\n' % (key, value))


