import os
from pathlib import Path
from queue import PriorityQueue
import heapq
import json

PQMAX = 5   # size of priority queue

data_folder = Path(os.path.dirname(__file__)).parent / "data"

def make_index(input_file):
    readfile = data_folder / input_file

    with open(readfile,"r",encoding='UTF8') as f:
        line = f.readline()
        prefix_dict = {}

        while line:
            word, count = line.split(':')
            if word == '':
                line = f.readline()
                continue
            for i in range(len(word)-1):    # word 자체는 prefix로 칠 필요 없음.
                if word[:i+1] not in prefix_dict:
                    prefix_dict[word[:i+1]] = PriorityQueue(PQMAX)

                pq = prefix_dict[word[:i+1]]

                if pq.full(): 
                    heapq.heappushpop(pq.queue,(int(count),word))
                else:
                    pq.put((int(count),word))   # multiply -1 to count so that least can come first in priority queue.

            line = f.readline()
        #end while

        for key,value in prefix_dict.items():
            word_list = [item[1] for item in value.queue]
            word_list = list(reversed(word_list))
            prefix_dict[key] = word_list

        return prefix_dict

        # for key, pq in prefix_dict.items():

        #     f.write('%s: ' % key)
        #     for i in range(pq.qsize()):
        #         item = pq.get()
        #         #f.write(item[1])   
        #         f.write('%s ' % (item[1]))
        #         #f.write('%s %d ' % (item[1],-item[0]))  # reverse the count to positive as it used to be.

        #     f.write('\n')

if __name__ == "__main__":
    prefix_dict = make_index("word_count.txt")
    writefile = data_folder / "prefix_dict.json"
    with open(writefile,"w") as json_file:
        json.dump(prefix_dict,json_file)