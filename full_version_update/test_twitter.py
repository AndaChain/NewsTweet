import unittest

from NLP_4test import NLP
from Twitter_API_4_test import Twitter_API

import traceback
import emoji
import csv
import time
from datetime import datetime, timedelta
from pythainlp.corpus.common import thai_words
import pandas
from bs4 import BeautifulSoup
import random

class Test(unittest.TestCase):
    def setUp(self):
        self.nlp = NLP()
        self.twitter = Twitter_API(self.nlp)
        self.start = time.time()

    # **********************************************twitter**********************************************
    def test_main_twitter(self):
        keyword = "covid"
        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_old = -1
        for i in reader:
            row_len_old += 1
        
        until = str(datetime.now()).split(" ")[0]
        self.twitter.main_twitter("all", 50, keyword, until, until)

        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_new = -1
        for i in reader:
            row_len_new += 1
        in_put = row_len_new
        #mode = "greater"
        condition = row_len_old

        self.assertGreater(in_put, condition)

    def test_hit_trends(self):
        self.twitter.hit_trends()
        read = open("Hit_Trends/Hit_Trends.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_new = -1
        for i in reader:
            row_len_new += 1
        in_put = row_len_new
        #mode = "notequal"
        condition = 0

        self.assertNotEqual(in_put, condition)

    def test_write_csv(self):
        keyword = "covid"
        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_old = -1
        for i in reader:
            row_len_old += 1
        
        #data = self.twitter.update_mode("crypto", "all", 50, "extended", "current", "2021-04-25", "2021-04-26")
        until = str(datetime.now()).split(" ")[0]
        OFFSET = 38555555555555
        data = self.twitter.api.search(q=keyword,
                                lang = "all",
                                count = 50,
                                tweet_mode = "extended",
                                result_type = "current",
                                max_id=str( 1-OFFSET-555555555-(100000000*1) ),
                                until=until)
        self.twitter.write_csv(data, "crypto", "all", until, until)

        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_new = -1
        for i in reader:
            row_len_new += 1
        in_put = row_len_new
        #mode = "greater"
        condition = row_len_old

        self.assertGreater(in_put, condition)
    # **********************************************twitter**********************************************

if( __name__ == "__main__"):
    unittest.main()

