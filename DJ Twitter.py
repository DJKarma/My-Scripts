import tweepy
import pandas as pd

col_names = ["UserName", "Location", "Reach", "Tweet", "TwittedAt"]
TweetDataFrame = pd.DataFrame(columns = col_names)
count = 1;

access_token = "1227163424964009984-scP3A0dLqTNwzXQijpT5zN3hTH3t0d"
access_token_secret = "pUGrJqPbmk9DkJJ9XLIWxtEr7lY6olW9QdTqoWoBbKbhk"
consumer_key = "jgaLfYEtJj0vlVzbQ5jTnHOVC"
consumer_secret = "39qx34kYNteFZq7A4mpiomA3j0MXkL7QhBdjoKEc0xTfAckvVa"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creating the API object while passing in auth information
#api = tweepy.API(auth,timeout=300,proxy = "http://USERNAME:PASSWORD@ci-proxy:80")
api = tweepy.API(auth,timeout=300,wait_on_rate_limit=True)

#initialize a list to hold all the tweepy Tweets
alltweets = []

newTweets  = api.search(q='@SouthernWater',count=300,tweet_mode='extended')

alltweets.extend(newTweets)
oldest = alltweets[-1].id - 1

while len(newTweets) > 0:
    # print("getting tweets before %s" % (oldest))
    newTweets  = api.search(q='@SouthernWater',count=300,tweet_mode='extended',max_id=oldest)
    alltweets.extend(newTweets)
    oldest = alltweets[-1].id - 1

# foreach through all tweets pulled
for tweet in alltweets:
   # printing the text stored inside the tweet object
   # print(tweet.user.screen_name,"Tweeted:",tweet.text)
    #print("The user Name:", tweet.user.name, "and Location is:",tweet.user.location, "Reach of:", tweet.user.followers_count,"Tweeted:",tweet.full_text,"Twitted At:", tweet.created_at)
    TweetDataFrame.at[count,"UserName"] = tweet.user.name
    TweetDataFrame.at[count,"Location"] = tweet.user.location
    TweetDataFrame.at[count,"Reach"] = tweet.user.followers_count
    TweetDataFrame.at[count,"Tweet"] = tweet.full_text
    TweetDataFrame.at[count,"TwittedAt"] = tweet.created_at
    count = count+1;

#print(TweetDataFrame)
TweetDataFrame.to_excel("tweets.xlsx")

print("Done")




from tweepy import streaming
from tweepy import StreamListener
from tweepy import OAuthHandler
import time



access_token = "1227163424964009984-scP3A0dLqTNwzXQijpT5zN3hTH3t0d"
access_token_secret = "pUGrJqPbmk9DkJJ9XLIWxtEr7lY6olW9QdTqoWoBbKbhk"
consumer_key = "jgaLfYEtJj0vlVzbQ5jTnHOVC"
consumer_secret = "39qx34kYNteFZq7A4mpiomA3j0MXkL7QhBdjoKEc0xTfAckvVa"



class listener (StreamListener):

    def on_data(self, data):
        try:
            print(data)
            savefile = open('pythontweet.csv', 'a')
            savefile.write(data)
            savefile.write("\n")
            savefile.close()
        except Exception as e:
            print(f"Failed on {e}")
            time.sleep(10)

        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
twitterStream = streaming.Stream(auth, listener())
twitterStream.filter(track=["SouthernWater"])
