import random
import sys
from datetime import datetime

DEFAULT_FILE = "randnums.txt"
DEFAULT_SIZE = 1024*1024*64

class GenRandNum:
    
    def __init__(self,filename,size):
        random.seed(datetime.now())
        self.write_file = filename
        self.size = size
    
    def write(self):
        with open(self.write_file,"w") as f:
            for i in range(int(self.size/sys.getsizeof(int))):
                f.write(str(random.randint(1,100000000))+' ')
    
if __name__ == "__main__":
    gen = GenRandNum(DEFAULT_FILE,DEFAULT_SIZE)
    gen.write()
    