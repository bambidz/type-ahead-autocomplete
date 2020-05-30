import os
from pathlib import Path
from queue import PriorityQueue
import heapq
import json

PQMAX = 5   # size of priority queue

# save index as versions in index_folder
index_folder = Path(os.path.dirname(__file__)).parent / "index"

class PrefixIndex:
    def __init__(self, **kwargs):
        self.readfile = kwargs["readfile"]
        self.qsize = kwargs["pqsize"]
        self.index = {}
        self.version = 1
        self.increment_version = 1
        self.delete_version = 1

    def load(self):
        with open(self.readfile,"r",encoding='UTF8') as f:
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
            self.index = prefix_dict

    # save index to the corresponing version folder.
    def save(self):
        index_version_folder = index_folder / str(self.version)
        Path(index_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = index_version_folder / "bulk_index.json"
        self.version += 1
        self.increment_version = 1
        if self.index: 
            with open(writefile,"w") as json_file:
                json.dump(self.index,json_file)

    def update(self,updated_prefixes):
        increment_version_folder = index_folder / str(self.version) / "incremental"
        Path(increment_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = increment_version_folder / ("incremental" + str(self.increment_version))
        with open(writefile,"w") as json_file:
            json.dump(updated_prefixes,json_file)

    def delete(self,deleted_prefixes):
        deleted_version_folder = index_folder / str(self.version) / "deleted"
        Path(deleted_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = deleted_version_folder / ("deleted" + str(self.increment_version))
        with open(writefile,"w") as json_file:
            json.dump(deleted_prefixes,json_file)
        
 