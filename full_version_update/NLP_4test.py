import os
import shutil

import pandas
import csv

# English
import spacy
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.sentiment import SentimentIntensityAnalyzer

# Thai
from pythainlp import word_tokenize, correct, Tokenizer
from pythainlp.util import isthai, normalize, dict_trie
from pythainlp.corpus.common import thai_words
from my_modul import Mymodul # sentiment Modul

# ใดๆ
import re
import emoji
from spacy_langdetect import LanguageDetector
import pickle 
import codecs
from numba import jit, int32

from manage_file import ManageFile
import time

class NLP:
    def __init__(self):
        # ----------------------NLP thai------------------------------------
        # stopwords_th.txt
        with codecs.open("dataset/stopwords_th.txt", "r", encoding="utf8") as f:
            lines = f.readlines()
        listpos=[e.strip() for e in lines]
        del lines
        f.close() # ปิดไฟล์

        self.stopwords_thai = listpos

        modul=self.loadData("Modul")
        print(modul)

        self.classifier = modul[0]
        self.vocabulary = modul[1]

        # คำไทย
        """read = open("dataset/thai_words.txt", "r")
        words = []
        add_words = set(thai_words())  # thai_words() returns frozenset
        for m in read:
            add_words.add(m.split("\n")[0])"""
        self.custom_tokenizer = dict_trie(thai_words())
        # ------------------------------------------------------------------

        # ----------------------NLP english------------------------------------
        self.nlp = spacy.load("en_core_web_md")

        self.sia = SentimentIntensityAnalyzer()

        self.STOP_WORD_1 = self.nlp.Defaults.stop_words # stop word ของ spacy

        self.STOP_WORD_2 = stopwords.words('english') # stop word ของ nltk
        self.STOP_WORD_3 = STOP_WORDS # stop word ของ spacy
        # ------------------------------------------------------------------

        # ----------------------detector--------------------------------------------
        self.nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
        # --------------------------------------------------------------------------

        self.dict_vocab = {i:False for i in self.vocabulary}

    def main_nlp(self, datas):
        """
            datas have to be list or something can for loop and got string that is content.
        """
        output_list = []
        out_STR = ""
        # --------------------------Filter all thing and return list of word "usefull"--------------------------------
        try:
            # ตัด #
            pattern  = re.compile(r"(#+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
            out_str_hashtags = pattern.sub("", datas)

            # ตัด @
            pattern  = re.compile(r"(@+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
            out_str_add = pattern.sub("", out_str_hashtags)

            # ตัด emoji
            str_output = emoji.get_emoji_regexp().sub(u'', out_str_add)

            # ตัด link
            pattern  = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
            out_str_link = pattern.sub("", str_output)  

            # ตัด ตัดอักษร+ตัวเลข
            pattern  = re.compile(r"([A-Za-z-_]+[\d]+[\w]*|[\d]+[A-Za-z-_]+[\w]*)")
            out_str_number = pattern.sub("", out_str_link)  

            # ตัด ตัวเลข
            pattern  = re.compile(r"([๑-๙(_)0-9]{1,})")
            out_str_ = pattern.sub("", out_str_number)

            out_STR += out_str_

            # หา #
            pattern  = re.compile(r"(?P<out_list>#+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
            output_list += re.findall(pattern, datas)

            # หา @
            pattern  = re.compile(r"(?P<out_list>@+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
            output_list += re.findall(pattern, datas)

            # หา ตัดอักษร+ตัวเลข
            pattern  = re.compile(r"(?P<out_list>[A-Za-z-_]+[\d]+[\w]*|[\d]+[A-Za-z-_]+[\w]*)")
            output_list += re.findall(pattern, datas)

        except AttributeError:
            pass
        # --------------------------Filter all thing and return list of word "usefull"--------------------------------
        #proc = deepcut.tokenize(out_STR)
        proc = word_tokenize(out_STR, engine="newmm", keep_whitespace=False, custom_dict=self.custom_tokenizer)
        for i in proc:
            # ----------------special symbol------------------
            special = re.compile(r"\W+").sub("",i) # special symbol
            if(special == "" or i.lower() == "https" or i.lower() == "http"):
                continue
            # ------------------------------------------------

            # -------------- stop word thai and english --------------
            if(isthai(i)):
                if( i not in self.stopwords_thai ):
                    output_list.append(i)
            elif(i.isascii()):
                if( i.lower() not in self.STOP_WORD_1 and i.lower() not in self.STOP_WORD_2 and i.lower() not in self.STOP_WORD_3 ):
                    output_list.append(i)
            # --------------------------------------------------------
        return output_list

    def detection_lang(self, data):
        doc = self.nlp(data)
        return doc._.language["language"]

    @jit
    def sentiment_eng(self, data):
        dict_ = self.sia.polarity_scores(data)
        if(dict_["compound"] > 0.0):
            return "pos"
        elif(dict_["compound"] < 0.0):
            return "neg"
        else:
            return "neu"

    @jit()
    def sentiment_thai(self, data):
        
        # array that has tokenize alredy.
        data = set(data)
        dict_vocab = self.dict_vocab.copy()
        for i in data:
            if(i in dict_vocab.keys()):
                dict_vocab[i] = True

        featurized_test_sentence =  dict_vocab
        print(len(featurized_test_sentence.keys()))
        return self.classifier.classify(featurized_test_sentence) # ใช้โมเดลที่ train ประมวลผล

    def storeData(self, db, name): 
        # database
        # Its important to use binary mode
        dbfile = open('dataset/'+name, 'wb') 

        # source, destination 
        pickle.dump(db, dbfile)                      
        dbfile.close()

    def loadData(self, name):
        # for reading also binary mode is important
        try:
            dbfile = open('dataset/'+name, 'rb')
            db = pickle.load(dbfile) 
            dbfile.close()
            return db
        except:
            self.storeData(Mymodul.main(), name)
            return self.loadData(name)

    def clear_name_places(self, in_str):
        # that use in clear places name that contain useless word emoji
        str_output = emoji.get_emoji_regexp().sub(u'', in_str)

        return str_output

if __name__ == "__main__":
        s = time.time()
        obj = NLP()
        #obj.storeData(Mymodul.main(), "Modul")
        print(time.time()-s)

# ref: https://stackoverflow.com/questions/43388476/how-could-spacy-tokenize-hashtag-as-a-whole
# ref: https://universaldependencies.org/docs/u/pos/
# ref: https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/

# ref: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# ref: https://medium.com/@m.treerungroj/machine-learning-supervised-learning-with-basic-scikit-learn-part1-99b8b2327c9
# ref: https://spacy.io/api/pipeline-functions#merge_entities
# ref: https://spacy.io/api/token

# ref: https://spacy.io/universe/project/spacy-langdetect
