import praw
import time
import sys
from PyQt5 import QtWidgets, uic
from nltk.corpus import stopwords
from maps import maps

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

class Ui(QtWidgets.QDialog):
    maps = maps()

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dashboard.ui', self)
        self.show()

        # get pointer to submit button
        self.button = self.findChild(QtWidgets.QPushButton, 'submit')
        self.button.clicked.connect(self.pressSubmit)

        # get pointers to tables
        self.dayTable = self.findChild(QtWidgets.QTableWidget, 'day')
        self.postTable = self.findChild(QtWidgets.QTableWidget, 'postTime')
        self.keyTable = self.findChild(QtWidgets.QTableWidget, 'keyWords')
        self.lenTable = self.findChild(QtWidgets.QTableWidget, 'length')

        # get pointer to input box
        self.input = self.findChild(QtWidgets.QLineEdit, 'subName')

    def pressSubmit(self):
        count(maps, reddit.subreddit(self.input.text()).top(limit=100, time_filter="year"))

        i = 0
        for value in maps.dayDict.values():
            self.dayTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
            i += 1

        i = 0
        for value in maps.timeDict.values():
            self.postTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
            i += 1

        i = 0
        for keys in dict(sorted(maps.topWords.items(), key=lambda item: item[1], reverse = True)).keys():
            self.keyTable.setItem(0, i, QtWidgets.QTableWidgetItem(keys))
            self.keyTable.setItem(1, i, QtWidgets.QTableWidgetItem(str(maps.topWords[keys])))
            i += 1
            if i == 10: break
        
        i = 0
        for keys in dict(sorted(maps.wordCount.items(), key=lambda item: item[1], reverse = True)).keys():
            self.lenTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(keys)))
            self.lenTable.setItem(1, i, QtWidgets.QTableWidgetItem(str(maps.wordCount[keys])))
            i += 1
            if i == 5: break

# get top 500 posts in last year of subreddit and add relevant items to dictionaries
def count(maps: maps, top, start = 0, end = time.time()):
    s = set(stopwords.words('english'))
    for post in top:
        utc = post.created_utc
        if utc >= start and utc <= end:
            day = time.strftime('%A', time.localtime(utc))
            hour = time.strftime('%H', time.localtime(utc))
            title = [x.lower() for x in post.title.split()] # make everything lowercase for filtering the stopwords
            filteredText = filter(lambda w: not w in s, title)

            maps.dayDict[day] = maps.dayDict.get(day, 0) + 1
            maps.timeDict[hour] = maps.timeDict.get(hour, 0) + 1
            maps.wordCount[len(title)] = maps.wordCount.get(len(title), 0) + 1
            
            for i in filteredText:
                maps.topWords[i] = maps.topWords.get(i, 0) + 1

# open and run UI
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()