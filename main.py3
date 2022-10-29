import praw
import time
from PyQt5 import QtWidgets, uic
import sys
from nltk.corpus import stopwords

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dashboard.ui', self)
        self.show()

        self.button = self.findChild(QtWidgets.QPushButton, 'submit')
        self.button.clicked.connect(self.pressSubmit)

        self.input = self.findChild(QtWidgets.QLineEdit, 'subName')

    def pressSubmit(self):
        top = reddit.subreddit(self.input.text()).top(limit=50, time_filter="year")
        count(top)

def count(top, start = 0, end = time.time()):
    dayDict = {}
    timeDict = {}
    wordCount = {}
    topWords = {}
    s = set(stopwords.words('english'))

    #top = reddit.subreddit(sub).top(limit=500, time_filter="year")
    for post in top:
        utc = post.created_utc
        if utc >= start and utc <= end:
            day = time.strftime('%A', time.localtime(utc))
            hour = time.strftime('%H', time.localtime(utc))
            title = [x.lower() for x in post.title.split()]
            filteredText = filter(lambda w: not w in s, title)

            dayDict[day] = dayDict.get(day, 0) + 1
            timeDict[hour] = timeDict.get(hour, 0) + 1
            wordCount[len(title)] = wordCount.get(len(title), 0) + 1
            
            for i in filteredText:
                topWords[i] = topWords.get(i, 0) + 1


    for key in dict(sorted(dayDict.items(), key=lambda item: item[1], reverse = True)):
        print(key + ": " + str(dayDict[key]))
    print()
    for key in sorted(timeDict.keys()):
        print(key + ": " + str(timeDict[key]))
    print()
    i = 0
    for key in dict(sorted(topWords.items(), key=lambda item: item[1], reverse = True)):
        print(str(key) + ": " + str(topWords[key]))
        i += 1
        if i == 10: break
    print()
    i = 0
    for key in dict(sorted(wordCount.items(), key=lambda item: item[1], reverse = True)):
        print(str(key) + ": " + str(wordCount[key]))
        i += 1
        if i == 5: break

    return dayDict

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()