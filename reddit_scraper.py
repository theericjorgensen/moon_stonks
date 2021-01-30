import praw
import json
import csv
from pymongo import MongoClient
from pprint import pprint

#Enter Reddit Account Info
client_id = ""
client_secret = ""
user_agent=""
username = ""
password=""

def create_reddit_object():
    
    reddit = praw.Reddit(client_id = "",client_secret = "",user_agent="",username="",password="")
    return reddit
    
reddit = create_reddit_object()

#Replace SatoshiStreetBets with whatever subreddit
subred = reddit.subreddit("SatoshiStreetBets")

"""
Hot is what's been getting a lot up upvotes/comments recently

New sorts post by the time of submission with the newest at the top of the page. It sorts new posts in the area of reddit you clicked the 'new' tab. So all.reddit.com/new gives you the latest post from the entirety (almost) of reddit. While clicking new in askreddit will give you their latest posts. This applies to all the tabs I explain below.

Rising is what is getting a lot of activity (comments/upvotes) right now. This is the category you are looking for.

Controversial is what's getting multiple downvotes and upvotes.

Top is what has gotten the most upvotes over the set period.

Gilded are just comments which have been given reddit gold by someone. Typically comments are gilded for being exceptionally informative, or funny, but someone can gild a comment for any reason at all. You could give gold (gild) a comment full of hate speech if you wanted to.
"""
#different reddit sorting categories
hot = subred.hot(limit=10)
new = subred.new(limit=10)
controv = subred.controversial(limit=10)
top = subred.top(limit=10)
gilded = subred.gilded(limit=10)

type(hot)

x = next(hot)
dir(x)

# MONGODB Information
connection = MongoClient('localhost',27107)
database = connection['reddit_crypto_posts']
collection = database['hot_posts']
test =  {"title":"title",
                    "author":"author",
                    "score":"score",
                    "time_created":"time_created"}
collection.insert_one(test)

#use a csv with crytpo name and symbol. can be replaced with a different csv
crypto_name = []
crypto_symbol = []
with open('cryto_coins.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        c_name = str(row[0]).lower()
        s_name = str(row[1]).lower()
        crypto_name.append(c_name)
        crypto_symbol.append(s_name)
print(crypto_name)
print("\n")
print(crypto_symbol)

for i in hot:
    reddit_post_dict = {}
    title = str(i.title).lower()
    author = str(i.author)
    score = int(i.score)
    time_created = str(i.created)
    
    res_symbol = any(ele in title for ele in crypto_symbol)
    res_name = any(ele in title for ele in crypto_name)
    if (res_symbol | res_name) :
        reddit_post_dict = {"title":title,
                    "author":author,
                    "score":score,
                    "time_created":time_created}
        collection.insert_one(reddit_post_dict)
        print(reddit_post_dict)
