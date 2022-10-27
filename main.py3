import praw
import time

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

def day_count(sub: str) -> dict:
    dayDict = {
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 0,
        'Sunday': 0
    }
    top = reddit.subreddit(sub).top(limit=500, time_filter="year")
    for post in top:
        day = time.strftime('%A', time.localtime(post.created_utc))
        dayDict[day] = dayDict.get(day) + 1

    #maxVal = max(dayDict.values())
    print("Number of posts per day in r/" + sub)
    for key in dayDict.keys():
        print(key + ": " + str(dayDict[key]))
    print()

    return dayDict

day_count("aww")
day_count("gaming")