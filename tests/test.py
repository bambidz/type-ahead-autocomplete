import unittest
from indexing import word_counter
from indexing import index_generator

class TestSum(unittest.TestCase):

    def test_word(self):
        wordfreq = word_counter.word_count("test_words.txt")
        test_answer = {'alex': 3, 'aman': 2, 'anaconda': 1, 'abigail': 1, 'abo': 1, 'and': 1, 'as': 1,'': 10}
        self.assertEqual(test_answer, wordfreq)

    def test_sum_tuple(self):
        prefix_dict = index_generator.make_index("test_index.txt")
        #print(prefix_dict)
        test_answer = {'a': ['as', 'alex', 'aman', 'and', 'anaconda'], 
        'al': ['alex'], 'ale': ['alex'], 'am': ['aman'], 'ama': ['aman'], 
        'an': ['and', 'anaconda'], 'ana': ['anaconda'], 'anac': ['anaconda'], 
        'anaco': ['anaconda'], 'anacon': ['anaconda'], 'anacond': ['anaconda'], 
        'ab': ['abo', 'abigail'], 'abi': ['abigail'], 'abig': ['abigail'], 
        'abiga': ['abigail'], 'abigai': ['abigail']}
        self.assertEqual(test_answer, prefix_dict)

if __name__ == '__main__':
    unittest.main()