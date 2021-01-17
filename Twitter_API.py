# test class
import tweepy
import csv

class Twitter_API:
    def __init__(self):

        # Key and token
        CONSUMER_KEY="ku1u0AkXp7DiD8UuDFBD5ejc7" # aka API key
        CONSUMER_SECRET="3OifKHMc5Ik7VMUhjoGUu4BZBDLRDLUTeM6Qo2M70OYKqHgpGP" # aka API key secret

        ACCESS_TOKEN="1348183052179001347-Sy8D0nHWqhVjKYiQ2cVTNgkv6m1HYW"
        ACCESS_TOKEN_SECRET="Tars6ymAzSCwLTTxGfeqR78cJTAhm7c7mfen5UAXKa1WQ"

        # Authenticate to Twitter
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create API object
        self.api = tweepy.API(self.auth, wait_on_rate_limit=False,
            wait_on_rate_limit_notify=True)

        # Write file .csv for checking and record infor
        self.csvfile = open('twitter_tweet.csv', 'w', newline='')
        fieldnames = ['places', 'time', 'tweet']
        self.writer = csv.DictWriter( self.csvfile, fieldnames=fieldnames )
        self.writer.writeheader()

    def search(self, lang):
        count_ = 0 # it's mean count how many tweet.
        maxId = 0 # starter id
        while(count_ < 1):
            try:
                query = "#covid19" # this is word that want to search
                lang = lang # language for search
                count = 5 # The number of results to try and retrieve per page. 
                tweet_mode = "extended"
                result_type = "mixed"
                data = self.api.search(q=query,
                                    lang=lang,
                                    count=count,
                                    tweet_mode=tweet_mode,
                                    result_type=result_type,
                                    max_id=str(maxId - 1))

                self.write_csv(data) # Write infor to .csv

                if(len(data)==0):
                    continue

                maxId = data[-1].id # ordering the tweet by id
                count_ += 1 # counter

            except tweepy.RateLimitError:
                if(input("Do you want quit? y/n?") == "y"):
                    break
                else:
                    pass
                
        print("Done",count_)
        self.csvfile.close()

    def write_csv(self, data):
        for infor in data:
            if(  (not infor.retweeted) and ("RT @" not in infor.full_text)  ):
                self.writer.writerow( {'places': infor.user.location, 'time': str(infor.created_at), 'tweet':infor.full_text} )

if __name__ == "__main__":
    obj = Twitter_API()
    obj.search()

# ref: https://chatbotslife.com/crawl-twitter-data-using-30-lines-of-python-code-e3fece99450e
# ref: http://docs.tweepy.org/en/latest/api.html?highlight=search#search-methods
# ref: https://web.archive.org/web/20170829051949/https://dev.twitter.com/rest/reference/get/search/tweets
# ref: http://docs.tweepy.org/en/latest/extended_tweets.html?highlight=retweet