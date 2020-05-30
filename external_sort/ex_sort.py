import os
import math

class ExSorter:
    
    def __init__(self,file,buffer_size,memory):
        self.file = file
        self.buffer_size = buffer_size
        self.memory = memory
        self.split_num = math.ceil(os.stat(self.file).st_size/self.memory)
    
    def split(self):
        with open(self.file,'r') as rf:
            for i in range(self.split_num):
                tmp_file = "_tmp"+str(i)
                with open(tmp_file,'a') as wf:
                    while os.stat(self.file).st_size<self.memory:
                        wf.append(rf.readline())

    def delete_tmp(self):
        for i in range(self.split_num):
            tmp_file = "_tmp"+str(i)
            os.remove(tmp_file)
                        

        # statinfo = os.stat(fname)
        # return statinfo.st_size

if __name__ == '__main__':
    exsort = ExSorter("randnums.txt",1024,1024*10)
    #exsort.split()
    #exsort.delete_tmp()