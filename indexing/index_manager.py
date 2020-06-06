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
        self.index = {}
        self.version = 1
        self.increment_version = 1
        self.delete_version = 1

    def load(self):
        for root, subdirs, files in os.walk(index_folder):
            subdirs = list(map(int, subdirs))
            latest_version = max(subdirs)
            self.version = latest_version
            break
        

        index_version_folder = index_folder / str(self.version)
        if os.path.isfile(index_version_folder / 'bulk_index.json'):
            with open(index_version_folder / 'bulk_index.json',"r",encoding='UTF8') as f:
                self.index = json.load(f)
        else : 
            print(index_version_folder / 'bulk_index.json')
            print('bulkfile does not exist')
            exit(-1)

        if os.path.isdir(index_version_folder / 'incremental'):
            for root, subdirs, files in os.walk(index_version_folder/'incremental'):
                for file in files:
                    filename = index_version_folder/'incremental'/file
                    with open(filename,"r",encoding='UTF8') as f:
                        update_dict = json.load(f)
                        for prefix, word in update_dict.items():
                            self.index[prefix].append(word)

        if os.path.isdir(index_version_folder / 'deleted'):
            for root, subdirs, files in os.walk(index_version_folder/'deleted'):
                for file in files:
                    filename = index_version_folder/'deleted'/file
                    with open(filename,"r",encoding='UTF8') as f:
                        update_dict = json.load(f)
                        for prefix, word in update_dict.items():
                            if word in self.index[prefix]:
                                self.index[prefix].remove(word)

    # # save index to the corresponing version folder.
    # def save(self):
    #     index_version_folder = index_folder / str(self.version)
    #     Path(index_version_folder).mkdir(parents=True, exist_ok=True)
    #     writefile = index_version_folder / "bulk_index.json"
    #     self.version += 1
    #     self.increment_version = 1
    #     if self.index: 
    #         with open(writefile,"w") as json_file:
    #             json.dump(self.index,json_file)
    def search(self,prefix):
        if prefix not in self.index:
            return None
        return self.index[prefix]

    def update(self,updated_prefixes):
        increment_version_folder = index_folder / str(self.version) / "incremental"
        Path(increment_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = increment_version_folder / ("incremental" + str(self.increment_version))
        self.increment_version +=1

        for prefix,word in updated_prefixes:
            self.index[prefix].append(word)

        with open(writefile,"w",encoding='UTF8') as json_file:
            json.dump(updated_prefixes,json_file)

    def delete(self,deleted_prefixes):
        deleted_version_folder = index_folder / str(self.version) / "deleted"
        Path(deleted_version_folder).mkdir(parents=True, exist_ok=True)
        writefile = deleted_version_folder / ("deleted" + str(self.increment_version))

        for prefix,word in deleted_prefixes:
            if word in self.index[prefix]:
                self.index[prefix].remove(word)

        self.delete_version +=1
        with open(writefile,"w",encoding='UTF8') as json_file:
            json.dump(deleted_prefixes,json_file)
        
 