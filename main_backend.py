from Twitter_API import *
from NLP_test2 import NLP_test
import time

class main(Twitter_API, NLP_test):
    def __init__(self):
        Twitter_API.__init__(self)
        NLP_test.__init__(self)

    def run(self, lang):
        self.search(lang)
        self.write_message(lang)

if __name__ == "__main__":
    clock = time.time()
    obj = main()
    obj.run("en")
    print( str(int(time.time())-int(clock)) + " sec" )