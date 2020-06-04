import os
import math
import sys

class ExSorter:
    
    def __init__(self,file,buffer_size,memory):
        self.file = file
        self.buffer_size = buffer_size
        self.memory = memory
        self.split_num = math.ceil(os.stat(self.file).st_size/self.memory)
    
    def split(self):
        with open(self.file,mode = 'r') as rf:
            for i in range(self.split_num):
                tmp_file = "_tmp"+str(i)
                with open(tmp_file,'a') as wf:
                    wrote=0
                    # incase last line wrote will exceed memory
                    while wrote<self.memory-100:  
                        line = rf.readline()
                        # \n is added in write.
                        wrote += sys.getsizeof(line)+1
                        wf.write(line)
                        

    def delete_tmp(self):
        for i in range(self.split_num):
            tmp_file = "_tmp"+str(i)
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
                        

        # statinfo = os.stat(fname)
        # return statinfo.st_size

if __name__ == '__main__':
    exsort = ExSorter("randnums.txt",1024,1024*10)
    exsort.delete_tmp()
    #exsort.split()