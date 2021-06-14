import unittest

from NLP_4test import NLP
from Website_crawler_14_2test import websites_crawler

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
        csv.field_size_limit(256<<20)
        self.nlp = NLP()
        self.websites_crawler = websites_crawler(self.nlp)
        self.websites_crawler.count = 1
        self.start = time.time()

    # **********************************************webcrawler**********************************************
    def test_main_crawler_not_update(self):
        keyword = "covid"
        until = str(datetime.now()).split(" ")[0]
        self.websites_crawler.main_crawler(keyword, "all", until, until)
        
        read = open("WebCrawler/"+keyword+"_cutall.csv","r")
        reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")

        row_len_new = -1
        for i in reader:
            row_len_new += 1
        in_put = row_len_new
        condition = 0

        self.assertNotEqual(in_put, condition)
        #self.test_programme( row_len_new, "notequal", 0 )

    def test_download_url_str(self):
        url = "https://www.bbc.com/"
        session = self.websites_crawler.get_session()
        resp = session.get(url)
        html_code = resp.content
        result = self.websites_crawler.download_url(html_code, url.split("/")[2], 1)
        in_put = len(result)
        condition = 0

        self.assertNotEqual(in_put, condition)
        #self.test_programme( len(result), "notequal", 0 )

    def test_download_url_byte(self):
        url = "https://www.bbc.com/"
        result = self.websites_crawler.download_url(url, url.split("/")[2], 1)
        in_put = len(result)
        condition = 0

        self.assertNotEqual(in_put, condition)
        #self.test_programme( len(result), "notequal", 0 )

    def test_analytics_url(self):
        url = "https://www.bbc.com/"
        result = self.websites_crawler.analytics_url(url, "", url.split("/")[2])
        in_put = result
        condition = "article"
        
        self.assertEqual(in_put, condition)
        #self.test_programme( result, "equal", "article" )
    
    def test_find_message(self):
        url = "https://www.bbc.com/"

        row_len_old = -3
        for j in range(3):
            temp = timedelta(days=j+1)
            #print(str(datetime.now()-temp).split(" ")[0])
            read = open("WebCrawler/Database/"+str(datetime.now()-temp).split(" ")[0]+".csv","r")
            reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
            for i in reader:
                row_len_old += 1
        
        session = self.websites_crawler.get_session()
        resp = session.get(url)
        html_code = resp.content
        temp = self.websites_crawler.find_message(html_code, url)

        row_len_new = -3
        for j in range(3):
            temp = timedelta(days=j+1)
            #print(str(datetime.now()-temp).split(" ")[0])
            read = open("WebCrawler/Database/"+str(datetime.now()-temp).split(" ")[0]+".csv","r")
            reader = csv.reader((line.replace('\0','') for line in read), delimiter=",")
            for i in reader:
                row_len_new += 1
        in_put = row_len_new
        condition = row_len_old

        self.assertGreater(in_put, condition)
        #self.test_programme( row_len_new, "greater", row_len_old )
    
    def test_find_time(self):
        url = "https://www.bbc.com/"
        date = str(datetime.now()).split(" ")[0]
        session = self.websites_crawler.get_session()
        resp = session.get(url)
        html_code = resp.content
        result = self.websites_crawler.find_time(html_code)
        in_put = result[0]
        condition = date

        self.assertEqual(in_put, condition)
        #self.test_programme( result[0], "equal", date )

    def test_find_topic(self):
        url = "https://www.bbc.com/"
        session = self.websites_crawler.get_session()
        resp = session.get(url)
        html_code = resp.content
        topic = self.websites_crawler.find_topic(html_code, url.split("/")[2])
        in_put = url not in topic
        condition = True

        self.assertTrue(in_put, condition)
        #self.test_programme( url not in topic, "true", True )

    def test_find_domain(self):
        url = "https://www.bbc.com/"
        result = self.websites_crawler.find_domain([url])
        in_put = result[0]
        condition = url.split("/")[2]

        self.assertEqual(in_put, condition)
        #self.test_programme( result[0], "equal", url.split("/")[2] )

    def test_link_format(self):
        url = "https://www.bbc.com/"
        result = self.websites_crawler.link_format(url, url.split("/")[2])
        in_put = "https://" in result or "http://" in result
        condition = True

        self.assertTrue(in_put, condition)
        #self.test_programme( "https://" in result or "http://" in result, "true", True )
    
    # **********************************************webcrawler**********************************************

if( __name__ == "__main__"):
    unittest.main()

