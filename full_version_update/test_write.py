import unittest

from NLP_4test import NLP
from manage_file import ManageFile

import traceback
import emoji
import csv
import time
from datetime import datetime, timedelta
from pythainlp.corpus.common import thai_words
import pandas
from bs4 import BeautifulSoup
import random
writefile = ManageFile("Test_write_file", "test", [0,1,2], "a")

class Test(unittest.TestCase):
    def setUp(self):
        self.nlp = NLP()
        self.start = time.time()

    # **********************************************write file**********************************************
    def test_managefile_main(self):
        row_len_old = -1
        read = open("Test_write_file/"+"test"+".csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        for i in reader:
            row_len_old += 1

        writefile = ManageFile("Test_write_file", "test", ["a","b","c"], "w")
        for i in range(random.randint(0,10), random.randint(11,100)):
            writefile.managefile_main( [i*0, i*1, i*2] )
        writefile.close()
        row_len_new = -1
        read = open("Test_write_file/"+"test"+".csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        for i in reader:
            row_len_new += 1

        self.assertGreater(row_len_new, row_len_old)

    def test_checking(self):
        row_len_old = -1
        read = open("Test_write_file/"+"test"+".csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        for i in reader:
            row_len_old += 1

        writefile = ManageFile("Test_write_file", "test", ["a","b","c"], "a")
        result = writefile.checking(["0","2","4"])

        self.assertTrue(result, True)
    
    def test_find_copy_tos(self):

        writefile = ManageFile("Test_write_file", "test", ["a","b","c"], "w")
        df = writefile.find_copy_to("1", "test", ["0","4"], ["a", "b"], self.nlp)

        self.assertIs(type(df), type(pandas.DataFrame(columns=["a","b","c"])))
    # **********************************************write file**********************************************
if( __name__ == "__main__"):
    unittest.main()

