# type-ahead-autocomplete


###word_counter.py
- read from gutenberg.txt
- create 'word:count' data
- write to word_count.txt


###index_generator.py
- read from word_count.txt
- create dictionary of 'prefix:priority queue'
- write to prefix_dict.txt


###searcher.py
- read from prefix_dict.txt
- input prefix from user
- print list of words related to the prefix if it exists
