import praw
import time

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

def day_count(top, start = 0, end = time.time()):
    dayDict = {}
    timeDict = {}
    #top = reddit.subreddit(sub).top(limit=500, time_filter="year")
    for post in top:
        utc = post.created_utc
        if utc >= start and utc <= end:
            day = time.strftime('%A', time.localtime(utc))
            hour = time.strftime('%H', time.localtime(utc))
            dayDict[day] = dayDict.get(day, 0) + 1
            timeDict[hour] = timeDict.get(hour, 0) + 1

    #maxVal = max(dayDict.values())
    for key in dayDict.keys():
        print(key + ": " + str(dayDict[key]))
    print()
    for key in timeDict.keys():
        print(key + ": " + str(timeDict[key]))

    return dayDict

top = reddit.subreddit("aww").top(limit=50, time_filter="year")
day_count(top)

# Filter by start date:
# a. Example: of the top 500 posts made in the last year, only analyze posts submitted after
# April 2nd inclusive.
# 2. Filter by end date:
# a. Example: of the top 500 posts made in the last year, only analyze posts submitted before
# October 13th inclusive.
# 3. Hours of the day: