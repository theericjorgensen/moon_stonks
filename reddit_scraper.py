import praw
import json
import csv
from pprint import pprint

with open('secrets.json') as secrets:
    secretData = json.load(secrets)

client_id = secretData.get('client_id')
client_secret = secretData.get('client_secret')
user_agent=secretData.get('user_agent')
username=secretData.get('username')
password=secretData.get('password')


def create_reddit_object():
    
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret, user_agent=user_agent, username=username, password=password)
    return reddit
    

def postTitleContains(name, symbol, title):
    if (name in title or symbol in title):
        return True
    return False
    

reddit = create_reddit_object()

#Replace SatoshiStreetBets with whatever subreddit
subred = reddit.subreddit("SatoshiStreetBets")

#different reddit sorting categories
hot = subred.hot(limit=10)
new = subred.new(limit=10)
controv = subred.controversial(limit=10)
top = subred.top(limit=10)
gilded = subred.gilded(limit=10)

x = next(hot)

#use a csv with crytpo name and symbol. can be replaced with a different csv
crypto_names = []
crypto_symbols = []
with open('cryto_coins.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        c_name = str(row[0]).lower()
        s_name = str(row[1]).lower()
        crypto_names.append(c_name)
        crypto_symbols.append(s_name)

posts = []

for each_post in hot:
    reddit_post_dict = {}
    title = str(each_post.title).lower()
    author = str(each_post.author)
    score = int(each_post.score)
    time_created = str(each_post.created)
    
    for index, name in enumerate(crypto_names):
        symbol = crypto_symbols[index]
        if postTitleContains(name, symbol, title):
            post = {"symbol": symbol,
                    "name": name,
                    "title": title,
                    "author": author,
                    "score": score,
                    "time_created": time_created
                    }
            posts.append(post)

pprint(posts)

