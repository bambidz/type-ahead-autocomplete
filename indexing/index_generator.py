import os
from pathlib import Path
from queue import PriorityQueue
import heapq
import json

PQMAX = 5   # size of priority queue

# save index as versions in index_folder
this_file = Path(os.path.abspath(__file__))
index_folder = Path(os.path.dirname(this_file)).parent / "index"

data_folder = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data"
print(data_folder)

class IndexGen:
    def __init__(self, **kwargs):
        self.readfile = data_folder / kwargs["readfile"]
        self.qsize = kwargs["pqsize"]
        self.index = {}
        self.version = kwargs["version"]

    def load(self):
        with open(self.readfile,"r",encoding='UTF8') as f:
            line = f.readline()
            prefix_dict = {}
            linecount = 0
            while line:
                word, count = line.split(':')
                if word == '':
                    line = f.readline()
                    continue
                #print("load mid yay")
                for i in range(len(word)-1):    # word 자체는 prefix로 칠 필요 없음.
                    if word[:i+1] not in prefix_dict:
                        prefix_dict[word[:i+1]] = PriorityQueue(PQMAX)
                    pq = prefix_dict[word[:i+1]]
                    if pq.full(): 
                        heapq.heappushpop(pq.queue,(int(count),word))
                    else:
                        pq.put((int(count),word))   # multiply -1 to count so that least can come first in priority queue.
                    linecount+=1
                    if linecount%10000==0:
                        print(linecount)
                line = f.readline()

            #print("load mid yay")
            #end while
            for key,value in prefix_dict.items():
                word_list = [item[1] for item in value.queue]
                word_list = list(reversed(word_list))
                prefix_dict[key] = word_list
            self.index = prefix_dict

    # save index to the corresponing version folder.
    def save(self):
        index_version_folder = index_folder / str(self.version)
        Path(index_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = index_version_folder / "bulk_index.json"
        if self.index: 
            with open(writefile,"w",encoding='UTF8') as json_file:
                json.dump(self.index,json_file)

if __name__ == '__main__':
    indexGen = IndexGen(
        readfile = "kor_word_count.txt",
        pqsize = 5,
        version = 4)
    print("number of words read: ")
    indexGen.load()
    print("yay")
    indexGen.save()

 