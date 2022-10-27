import praw

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

def fetch_subreddit(subreddit):   
    print("test subreddit")

def fetch_filters(filters):
    print("test filters")

fetch_subreddit("aww")

hot_posts = reddit.subreddit('MachineLearning').top(limit=5, time_filter="month")
for post in hot_posts:
   print(post.title)