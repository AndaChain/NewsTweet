from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import codecs
from itertools import chain

class Mymodul:
  def main():

    # pos.txt
    with codecs.open('dataset/pos2.txt', 'r', "utf-8") as f:
      lines = f.readlines()
    listpos=[e.strip() for e in lines]
    del lines
    f.close() # ปิดไฟล์

    # neg.txt
    with codecs.open('dataset/neg2.txt', 'r', "utf-8") as f:
      lines = f.readlines()
    listneg=[e.strip() for e in lines]
    del lines
    f.close() # ปิดไฟล์

    # neutral.txt
    with codecs.open('dataset/neutral2.txt', 'r', "utf-8") as f:
      lines = f.readlines()
    listneutral=[e.strip() for e in lines]
    del lines
    f.close() # ปิดไฟล์


    pos1=['pos']*len(listpos)
    neg1=['neg']*len(listneg)
    neutral1=["neu"]*len(listneutral)

    training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1)) + list(zip(listneutral,neutral1))
  
    vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))

    feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
  
    classifier = nbc.train(feature_set)
    a = (classifier,vocabulary)
    return a