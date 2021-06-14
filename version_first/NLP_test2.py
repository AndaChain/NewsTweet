import re
import spacy
import csv
from pythainlp import word_tokenize

class NLP_test:
    def __init__(self):
        # Write file .csv for checking and record infor
        self.csvfile_output = open('tweet_NLP_2.csv', 'w', newline='', encoding="utf-8")
        self.csvfile_input = open('twitter_tweet.csv', 'r')
        self.csv_reader = csv.reader(self.csvfile_input, delimiter=',')

        fieldnames = ['word', 'number']
        self.writer_output = csv.DictWriter( self.csvfile_output, fieldnames=fieldnames )
        self.writer_output.writeheader()

        #self.th_or_en = False # False is english, True is Thai

    def regular(self, data):
        output = []
        nlp = spacy.load("en_core_web_md")
        docs = nlp(data)
                
        # search a index hashtag and end a index hashtag.
        indexes = [m.span() for m in re.finditer('#\w+',data,flags=re.IGNORECASE)]
        
        # merge hashtag and word
        for start,end in indexes:
            docs.merge(start_idx=start,end_idx=end)

        # for filter words that don't use for search
        for word in docs:
            if( self.filter_type(word) ): # word is one of spacy
                output.append(word.text)
                
        return output

    def regular_th(self, data):
        proc = word_tokenize(data, engine='newmm')
        return proc

    def filter_type(self, word):

        type_word = ["ADJ", "INTJ",
                    "NOUN", "PROPN", "VERB", "NUM"]

        # if any words is one of type word that use for search.
        if( word.pos_ in type_word ):
            return True
        else:
            return False
                
    def write_message(self, lang):
        dict_temp = {}
                
        # select only tweet ==> merge word and hashtag
        # ==> filter by type ==> write .csv file by word and number

        for row in self.csv_reader: # select only twee
            if(lang == "th"):
                temp = self.regular_th(row[2]) # merge word and hashtag ==> filter by type
            elif(lang == "en"):
                temp = self.regular(row[2]) # ใช้ของภาษาไทย
                
            for i in temp[1:]:
                message = i.lower()
                if( message not in dict_temp ): # dictionary for count word
                    dict_temp[message] = 1
                elif( message in dict_temp ):
                    dict_temp[message] += 1

        # write .csv file by word and number
        for temp in dict_temp:
            self.writer_output.writerow({'word':temp, 'number':dict_temp[temp]})

        self.csvfile_output.close()
        self.csvfile_input.close()

if __name__ == "__main__":
        obj = NLP_test()
        obj.write_message()

# ref: https://stackoverflow.com/questions/43388476/how-could-spacy-tokenize-hashtag-as-a-whole
# ref: https://universaldependencies.org/docs/u/pos/
# ref: https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/