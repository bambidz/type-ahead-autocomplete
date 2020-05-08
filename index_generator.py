from queue import PriorityQueue

if __name__ == "__main__":
    
    PQMAX = 5          # size of priority queue

    f = open("word_count.txt","r",encoding='UTF8')
    #word_list
    content = f.read()
    f.close()
    prefix_dict = {}

    lines = content.split('\n')

    for line in lines:

        if line == "":
            continue

        word, count = line.split(':')

        for i in range(len(word)-1):    # word 자체는 prefix로 칠 필요 없음.
            if word[:i+1] not in prefix_dict:
                prefix_dict[word[:i+1]] = PriorityQueue(PQMAX)

            pq = prefix_dict[word[:i+1]]

            if pq.full(): 

                max = -99999
                kick_index = 0
                for i in range(PQMAX):
                    if max < pq.queue[i][0]:
                        max = pq.queue[i][0]
                        kick_index = i
                # end for

                if max<-int(count):
                    continue
                else:
                    del pq.queue[kick_index]

            pq.put((-int(count),word))   # multiply -1 to count so that least can come first in priority queue.
        


    f = open("prefix_dict.txt","w",encoding='UTF8')

    for key, pq in prefix_dict.items():
        f.write('%s: ' % key)
        for i in range(pq.qsize()):
            item = pq.get()
            f.write('%s ' % (item[1]))   
            #f.write('%s %d ' % (item[1],-item[0]))  # reverse the count to positive as it used to be.
        
        f.write('\n')

    f.close()

