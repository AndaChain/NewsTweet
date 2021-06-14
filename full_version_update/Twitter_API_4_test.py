# test class
import tweepy
import csv
from datetime import timedelta
from datetime import datetime
import re

from manage_file import ManageFile
from NLP_4test import NLP

import time

class Twitter_API:
    def __init__(self, nlp):
        # Key and token
        CONSUMER_KEY="ku1u0AkXp7DiD8UuDFBD5ejc7" # aka API key
        CONSUMER_SECRET="3OifKHMc5Ik7VMUhjoGUu4BZBDLRDLUTeM6Qo2M70OYKqHgpGP" # aka API key secret

        ACCESS_TOKEN="1348183052179001347-Sy8D0nHWqhVjKYiQ2cVTNgkv6m1HYW"
        ACCESS_TOKEN_SECRET="Tars6ymAzSCwLTTxGfeqR78cJTAhm7c7mfen5UAXKa1WQ"

        # Authenticate to Twitter
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create API object
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)

        self.nlp2 = nlp

    def main_twitter(self, lang, count, keyword, since, until, update=False):
        # ค่าคงที่
        OFFSET = 38555555555555
        # start open file "a" mode
        column = ['time', 'content', 'places']
        self.writer2 = ManageFile("Twitter", keyword+"_Ncut"+lang, column, "a")
        self.date_since = datetime.strptime(since+" 00:00:00", "%Y-%m-%d %H:%M:%S")
        until = datetime.strptime(until, "%Y-%m-%d")+timedelta(days=1)
        until = str(until).split(" ")[0]

        count_ = 0 # it's mean count how many tweet.
        maxId = -1 # starter id
        moreOFFSET = 0
        tricker = True

        query = keyword # this is word that want to search
        count = count # The number of results to try and retrieve per page. 
        tweet_mode = "extended"
        result_type = "current"

        # when update mode is active
        while(tricker):
            print(count_, "round Twitter")
            print(count_)
            try:
                # print("ok1")
                if( maxId <= 0 and moreOFFSET < 1 ):
                    # รอบแรก
                    data = self.api.search(q=query,
                                                lang = lang,
                                                count=count,
                                                tweet_mode=tweet_mode,
                                                result_type=result_type,
                                                until=until)
                else:
                    # รอบต่อๆไป
                    if(moreOFFSET >= 1):
                        # OFFSET เพิ่มเรื่อยๆๆๆๆ
                        data = self.api.search(q=query,
                                                    lang = lang,
                                                    count=count,
                                                    tweet_mode=tweet_mode,
                                                    result_type=result_type,
                                                    max_id=str( maxId-OFFSET-555555555-(100000000*moreOFFSET) ), # a x 10^13
                                                    until=until)
                        count_ += 1
                        moreOFFSET += 1
                    else:
                        # OFFSET ค่าคงที่
                        data = self.api.search(q=query,
                                                    lang = lang,
                                                    count=count,
                                                    tweet_mode=tweet_mode,
                                                    result_type=result_type,
                                                    max_id=str(maxId-OFFSET), # a x 10^13
                                                    until=until)
                # print("ok2")
                maxId = data[-1].id
                count_ += 1 # counter
                tricker = self.write_csv(data, keyword, lang, since, until) # Write infor to .csv
            except IndexError:
                # เมื่อ data[-1].id IndexError หรือก็คือไม่มี tweet ไหนเลยที่หาได้เลย
                # print("no data")
                moreOFFSET += 1
                count_ += 1
                if(count_ >= 10):
                    tricker = False
            except tweepy.error.TweepError:
                pass

        self.writer2.close()
        print("Twitter Done",count_)

    def update_mode(self, query, lang, count, tweet_mode, result_type, since, until):
        data = tweepy.Cursor(self.api.search,q=query,
                                    lang = lang,
                                    count=count,
                                    tweet_mode=tweet_mode,
                                    result_type=result_type,
                                    until=until).items()
        
        #tricker = self.write_csv(data, query, lang, since, until)
        return data

    def write_csv(self, data, keyword, lang, since, until):
        # Write file .csv for checking and record infor
        """column = ['time', 'content', 'places']
        self.writer2 = ManageFile("Twitter", keyword+"_Ncut"+lang, column, "a")
        self.date_since = datetime.strptime(since+" 00:00:00", "%Y-%m-%d %H:%M:%S")"""

        for infor in data:
            date_created_at = datetime.strptime(str(infor.created_at), "%Y-%m-%d %H:%M:%S")
            #print(date_created_at, self.date_since)
            # when update mode is active time is ignore
            if( date_created_at < self.date_since ):
                #print(date_created_at, self.date_since, "<")
                return False

            all_lang = self.nlp2.detection_lang(infor.full_text)
            check_lang = lang == all_lang
            if(lang == "all"):
                check_lang = ("en" == all_lang) or ("th" == all_lang)
            if( ("RT @" not in infor.full_text) and check_lang ):
                #print([str(infor.created_at), infor.full_text, infor.user.location])
                self.writer2.managefile_main( [str(infor.created_at), infor.full_text, infor.user.location] )
                #writerow( {'places': infor.user.location, 'time': str(infor.created_at), 'message':infor.full_text, 'link':"-"} )
        return True
    def hit_trends(self):
        start = time.time()
        
        column = ["keyword", "tweet"]

        writer = ManageFile("Hit_Trends", "Hit_Trends", column, "w")

        # WOEID of Bangkok
        woeid = 1225448

        # fetching the trends 
        trends = self.api.trends_place(id = woeid) 

        # printing the information 
        print("The top trends for the location are :") 
        
        for value in trends:
            for trend in value['trends']:
                writer.managefile_main([trend["name"], trend["tweet_volume"]])
                #print(trend["name"], trend["tweet_volume"])
        
        print(time.time()-start, "hittwitter")
if __name__ == "__main__":
    obj = Twitter_API(NLP())
    obj.main_twitter("all", 50, "covid", "2021-04-25", "2021-04-29")
    #obj.update_mode()

# ref: https://chatbotslife.com/crawl-twitter-data-using-30-lines-of-python-code-e3fece99450e
# ref: http://docs.tweepy.org/en/latest/api.html?highlight=search#search-methods
# ref: https://web.archive.org/web/20170829051949/https://dev.twitter.com/rest/reference/get/search/tweets
# ref: http://docs.tweepy.org/en/latest/extended_tweets.html?highlight=retweet