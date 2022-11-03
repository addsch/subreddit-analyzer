import praw
import sys
import time
from datetime import datetime
from dictionaries import dictionaries
from nltk.corpus import stopwords
from PyQt5 import QtWidgets, uic

reddit = praw.Reddit(client_id='yFbFjg4Wni1j3PEixNSZzQ',
                     client_secret='kOyCoHbX4Cx4C5Df59jf8M47uCzRSQ',
                     user_agent='web-app:frontend-redditAPI-challenge:v1')

class Ui(QtWidgets.QDialog):
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

        # get pointers to start and end date filters
        self.startDateInp = self.findChild(QtWidgets.QDateEdit, 'startDate')
        self.endDateInp = self.findChild(QtWidgets.QDateEdit, 'endDate')

        # get points to start and end hour filters
        self.startTimeInp = self.findChild(QtWidgets.QTimeEdit, 'startTime')
        self.endTimeInp = self.findChild(QtWidgets.QTimeEdit, 'endTime')

        # get pointer to input box
        self.input = self.findChild(QtWidgets.QLineEdit, 'subName')

    def pressSubmit(self):
        dicts = dictionaries()

        # convert start and end filters to UTC epoch
        startEpoch = datetime.strptime(self.startDateInp.text(), "%m/%d/%Y").timestamp()
        endEpoch = datetime.strptime(self.endDateInp.text(), "%m/%d/%Y").timestamp()

        # remove ':' from start and end time inputs
        startTime = self.startTimeInp.text()[0:2] + self.startTimeInp.text()[3:5]
        endTime = self.endTimeInp.text()[0:2] + self.endTimeInp.text()[3:5]

        # get top 500 posts of subreddit
        top = reddit.subreddit(self.input.text()).top(limit=500, time_filter="year")

        # call API and store all relevant items in dictionaries
        fetch(dicts, top, startEpoch, endEpoch, int(startTime), int(endTime))

        # print the results into the tables of the ui
        i = 0
        for value in dicts.dayDict.values():
            self.dayTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
            i += 1

        i = 0
        for value in dicts.timeDict.values():
            self.postTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
            i += 1

        i = 0
        for keys in dict(sorted(dicts.topWords.items(), key=lambda item: item[1], reverse = True)).keys():
            self.keyTable.setItem(0, i, QtWidgets.QTableWidgetItem(keys))
            self.keyTable.setItem(1, i, QtWidgets.QTableWidgetItem(str(dicts.topWords[keys])))
            i += 1
            if i == 10: break
        
        i = 0
        for keys in dict(sorted(dicts.wordCount.items(), key=lambda item: item[1], reverse = True)).keys():
            self.lenTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(keys)))
            self.lenTable.setItem(1, i, QtWidgets.QTableWidgetItem(str(dicts.wordCount[keys])))
            i += 1
            if i == 5: break
        dicts.reset()

# get top 500 posts in last year of subreddit and add relevant items to dictionaries
def fetch(maps: maps, top, startDay, endDay, startTime, endTime):
    # get stopwords for filtering out unwanted common words
    s = set(stopwords.words('english'))

    for post in top:
        utc = post.created_utc
        timePosted = int(datetime.fromtimestamp(utc).strftime('%H%M'))

        if utc >= startDay and utc <= endDay and timePosted >= startTime and timePosted <= endTime:
            day = time.strftime('%A', time.localtime(utc))
            hour = time.strftime('%H', time.localtime(utc))

            # make everything lowercase for filtering the stopwords
            title = [x.lower() for x in post.title.split()] 
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