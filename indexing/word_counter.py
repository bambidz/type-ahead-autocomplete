#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import collections
import os
from pathlib import Path

data_folder = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data"

def word_count(input_file,output_file):
    readfile = data_folder / input_file
    wordfreq = collections.Counter()
    with open(readfile,"r",encoding = "UTF8") as f:
        line_data = f.readline()
        while line_data:
            words_in_line = re.split('[^a-zA-Z0-9]+', line_data)
            words_in_line = ([ word.lower() for word in words_in_line ])
            wordfreq.update(words_in_line)
            line_data = f.readline()

    writefile = data_folder / output_file
    with open(writefile,"w",encoding = "UTF8") as f:
        for key, value in wordfreq.items():
            f.write('%s:%s\n' % (key, value))

def kor_word_count(input_file,output_file):
    readfile = data_folder / input_file
    wordfreq = collections.Counter()
    print(readfile)
    with open(readfile,"r",encoding = "UTF8") as f:
        line_data = f.readline()
        while line_data:
            words_in_line = re.split("[^가-힣]", line_data)
            words_in_line = ([ korean_to_be_englished(word) for word in words_in_line ])
            wordfreq.update(words_in_line)
            line_data = f.readline()

    writefile = data_folder / output_file
    with open(writefile,"w",encoding = "UTF8") as f:
        for key, value in wordfreq.items():
            f.write('%s:%s\n' % (key, value))

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def korean_to_be_englished(korean_word):
    r_lst = []
    dissected_word = ""
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
            dissected_word += CHOSUNG_LIST[ch1] + JUNGSUNG_LIST[ch2] + JONGSUNG_LIST[ch3]
        else:
            r_lst.append([w])
            

        
    return dissected_word
    
# korean_to_be_englished("이승훈a")

if __name__ == "__main__":
    
    kor_word_count("naver_movie_review.txt","kor_word_count.txt")
