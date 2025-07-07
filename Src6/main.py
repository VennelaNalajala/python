import tweepy
import configparser
from connection import sqlserver
 
token=configparser.ConfigParser(interpolation=None)
token.read('config.ini')
bearer_token = token['twitter']['bearer']
 
client = tweepy.Client(bearer_token=bearer_token)
 
username = "revanth_anumula"
 
 
user = client.get_user(username=username)
user_id = user.data.id
fetch=sqlserver()
cursor1=fetch.cursor()
cursor1.execute("SELECT MAX(id) FROM twitter")
last_id = cursor1.fetchone()[0]
tweets = client.get_users_tweets(id=user_id,since_id=last_id, max_results=5,tweet_fields=['created_at'])
 
conn=sqlserver()
cursor=conn.cursor()
 
for tweet in tweets.data:
    tweet_id=tweet.id
    tweet_text=tweet.text
    tweet_date=tweet.created_at
 
    cursor.execute("insert into twitter (id,content,post_time) values (?,?,?)",tweet_id,tweet_text,tweet_date)
conn.commit()
conn.close()
print("twets updated")
 
 
 
 