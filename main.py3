import praw
import time

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

def count(top, start = 0, end = time.time()):
    dayDict = {}
    timeDict = {}
    wordCount = {}
    #top = reddit.subreddit(sub).top(limit=500, time_filter="year")
    for post in top:
        utc = post.created_utc
        if utc >= start and utc <= end:
            day = time.strftime('%A', time.localtime(utc))
            hour = time.strftime('%H', time.localtime(utc))
            title = len(post.title.split())
            dayDict[day] = dayDict.get(day, 0) + 1
            timeDict[hour] = timeDict.get(hour, 0) + 1
            wordCount[title] = wordCount.get(title, 0) + 1

    for key in dict(sorted(dayDict.items(), key=lambda item: item[1], reverse = True)):
        print(key + ": " + str(dayDict[key]))
    print()
    for key in sorted(timeDict.keys()):
        print(key + ": " + str(timeDict[key]))
    print()
    i = 0
    for key in dict(sorted(wordCount.items(), key=lambda item: item[1], reverse = True)):
        print(str(key) + ": " + str(wordCount[key]))
        i += 1
        if i == 5: break

    return dayDict

top = reddit.subreddit("aww").top(limit=50, time_filter="year")
count(top)