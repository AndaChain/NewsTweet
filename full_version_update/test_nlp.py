import unittest

from NLP_4test import NLP

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
        self.start = time.time()

    # **********************************************NLP**********************************************
    def test_main_nlp(self):
        print("*****test_main_nlp*****")

        datas = "ตอนนี้อาจารย์กำลังรอให้เพื่อนคุณคนนึง ส่งเมล์ยืนยันกลับมาว่าทราบเรื่องการสอบ และส่ง Microsoft Account มาให้อจ. เพิ่มเข้าไปในผู้เข้าสอบ (อจ. จะเพิ่มเป็นไฟล์ ทำทีเดียวเลย น่าจะทำการเพิ่มได้เสร็จภายในวันนี้) - ข้อสอบ เป็นแบบให้พิมพ์คำตอบด้วยคีย์บอร์ด มีทั้งหมด 30 ข้อ 160 คะแนน โดยแต่ละข้อจะบอกคะแนนกำกับไว้แล้ว"
        made = self.nlp.main_nlp(datas)
        in_put = type(made)
        #mode = "equal"
        condition = type(list())

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_main_nlp*****")

    def test_detection_lang(self):
        print("*****test_detection_lang*****")

        datas = "ตอนนี้อาจารย์กำลังรอให้เพื่อนคุณคนนึง ส่งเมล์ยืนยันกลับมาว่าทราบเรื่องการสอบ และส่งMicrosoft Account มาให้อจ. เพิ่มเข้าไปในผู้เข้าสอบ (อจ. จะเพิ่มเป็นไฟล์ ทำทีเดียวเลย น่าจะทำการเพิ่มได้เสร็จภายในวันนี้) - ข้อสอบ เป็นแบบให้พิมพ์คำตอบด้วยคีย์บอร์ด มีทั้งหมด 30 ข้อ 160 คะแนน โดยแต่ละข้อจะบอกคะแนนกำกับไว้แล้ว"
        lang = "th"
        made = self.nlp.detection_lang(datas)
        in_put = made
        #mode = "equal"
        condition = lang

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_detection_lang*****")

    def test_sentiment_eng(self):
        print("*****test_sentiment_eng*****")

        datas = "The power of modern search engines is undeniable: you can summon knowledge from the internet at a moment’s notice. Unfortunately this superpower isn’t omnipresent. There are many situations where search is relegated to strict keyword search or when the objects aren’t text search may not be available. Furthermore strict keyword search doesn’t allow the user to search semantically which means information is not as discoverable."
        mode = "neu"
        in_put = self.nlp.sentiment_eng(datas)
        #mode2 = "equal"
        condition = mode

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_sentiment_eng*****")
    
    def test_sentiment_thai(self):
        print("*****test_sentiment_thai*****")

        datas = "ตอนนี้อาจารย์กำลังรอให้เพื่อนคุณคนนึง ส่งเมล์ยืนยันกลับมาว่าทราบเรื่องการสอบ และส่งMicrosoft Account มาให้อจ. เพิ่มเข้าไปในผู้เข้าสอบ (อจ. จะเพิ่มเป็นไฟล์ ทำทีเดียวเลย น่าจะทำการเพิ่มได้เสร็จภายในวันนี้) - ข้อสอบ เป็นแบบให้พิมพ์คำตอบด้วยคีย์บอร์ด มีทั้งหมด 30 ข้อ 160 คะแนน โดยแต่ละข้อจะบอกคะแนนกำกับไว้แล้ว"
        mode = "neu"
        result = self.nlp.main_nlp(datas)
        temp = self.nlp.sentiment_thai(result)
        in_put = temp
        #mode = "equal"
        condition = mode

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_sentiment_thai*****")

    def test_loadData_and_storeData(self):
        print("*****test_loadData_and_storeData*****")

        datas = [123]
        self.nlp.storeData(datas, "ลบออก")
        in_put = self.nlp.loadData("ลบออก")
        #mode = "equal"
        condition = datas

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_loadData_and_storeData*****")

    def test_clear_name_places(self):
        print("*****test_clear_name_places*****")
        #pattern = [str(i) for i in range(10)]
        datas = "🇫🇷 Bastille Day 🎂 Birthday 🛍️ Black Friday ✊🏿 Black Lives Matter 🇨🇦 Canada Day 🇧🇷 Carnaval 🐉 Chinese New Year 🎅 Christmas🇲🇽 Cinco de Mayo 🦠 Coronavirus"
        result = self.nlp.clear_name_places(datas)
        in_put = emoji.get_emoji_regexp().search(result)
        #mode = "equal"
        condition = None

        print(f'{in_put}, {condition} OK')
        self.assertEqual(in_put, condition)
        print("*****test_clear_name_places*****")
    # **********************************************NLP**********************************************

if( __name__ == "__main__"):
    unittest.main()

