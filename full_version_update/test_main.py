import unittest

from manage_file import ManageFile
from main_backend_test6nof import main

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
        #0.5107500315791341
        #0.1749795049563792
        #443 305.29584097862244
        #Ran 2 tests in 327.710s
        self.main = main()
    
    def test_go_twitter(self):
        keyword = "นายก"
        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_old = -1
        for i in reader:
            row_len_old += 1
        
        until = str(datetime.now()+timedelta(days=1)).split(" ")[0]
        self.main.go_twitter("all", 50, keyword, "2021-04-30", "2021-05-02")

        read = open("Twitter/"+keyword+"_Ncutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_new = -1
        for i in reader:
            row_len_new += 1
        in_put = row_len_new
        #mode = "greater"
        condition = row_len_old

        self.assertGreater(in_put, condition)

    def test_cut_text(self):
        keyword = "โควิด"
        folder = "WebCrawler"
        lang = "all"
        read = open("GUI_show/"+keyword+"_ranking_"+str(folder).lower()+lang+".csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_old = -1
        for i in reader:
            row_len_old += 1
        self.main.array_sentiment = []
        self.main.array_sentiment_twi = []
        self.main.array_sentiment_web = []
        since = str(datetime.now()-timedelta(days=1)).split(" ")[0]
        until = str(datetime.now()).split(" ")[0]
        print(since, until)
        #self.main.run_webcrawler(lang, keyword, since, until)
        self.main.cut_text(folder, keyword, ["time","content","places"], lang, "2021-04-30", "2021-05-02")

        read = open("GUI_show/"+keyword+"_ranking_"+str(folder).lower()+lang+".csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
        row_len_new = -1
        for i in reader:
            row_len_new += 1

        in_put = row_len_new
        #mode = "greater"
        condition = row_len_old

        self.assertGreater(in_put, condition)
if( __name__ == "__main__"):
    unittest.main()

