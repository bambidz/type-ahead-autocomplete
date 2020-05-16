#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import collections
import os
from pathlib import Path

data_folder = Path(os.path.dirname(__file__)).parent / "data"

def word_count(input_file):
    readfile = data_folder / input_file
    wordfreq = collections.Counter()
    with open(readfile,"r",encoding = "UTF8") as f:
        line_data = f.readline()
        while line_data:
            words_in_line = re.split('[^a-zA-Z0-9]+', line_data)
            words_in_line = ([ word.lower() for word in words_in_line ])
            wordfreq.update(words_in_line)
            line_data = f.readline()

    return wordfreq

if __name__ == "__main__":
    
    wordfreq = word_count("gutenburg.txt")
    writefile = data_folder / "word_count.txt"
    with open(writefile,"w",encoding = "UTF8") as f:
        for key, value in wordfreq.items():
            f.write('%s:%s\n' % (key, value))