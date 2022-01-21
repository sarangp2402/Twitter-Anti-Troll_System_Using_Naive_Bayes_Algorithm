# import the Flask class from the flask module
import flask
from flask import Flask, render_template, redirect, url_for, request ,make_response
from flask import Flask, make_response
#from flask import Flask
from flask import request
from flask import render_template
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
# create the application object
app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
import os
import re
import pandas as pd
import numpy as np
import sns as sns
import base64
import tweepy
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from textblob import TextBlob
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#from textblob import TextBlob
import nltk
import oauth2
import urllib.parse
import base64
import twitter
import json
#import sentiment_mod as s
#import MySQLdb
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import mysql.connector
from mysql.connector import Error
import time
from nltk.corpus import stopwords
import re
import seaborn as sns
import datetime
from datetime import datetime
from datetime import timedelta
from io import StringIO
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pdfkit

connection = mysql.connector.connect(host='localhost', database='twitteranalysis', user='root', password='')
db_Info = connection.get_server_info()
print("Connected to MySQL Server version ", db_Info)
cursor = connection.cursor()
cursor.execute("select database();")
record = cursor.fetchone()
print("You're connected to database: ", record)
cursor.execute("SELECT COUNT(*) FROM twitterdata")
rowcount = cursor.fetchone()[0]
print(rowcount)

consumer_key = 'AQxIHlYTiJUh9DRvxdpzECwti'
consumer_secret = 'Sy0sB1RlYfFrkqhe9gw6nGdvamw2rQz3W1JWQL8lvrfK939vBb'
access_token = '1167423074678870018-2kAL2dDe89OeqWuwi1uJ9Yt6KqE1bo'
access_token_secret = 'II39fX59Ehxx5vcytC5F07RkD5Z2w12tXaWPzpMxKFc1p'
cursor = connection.cursor()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

apl = tweepy.API(auth)

def search(keyword):

    class listener(StreamListener):
        def __init__(self):
            super(StreamListener, self).__init__()
            super().__init__()
            self.counter = rowcount
            self.limit = rowcount + 25

        def on_data(self, data):
            all_data = json.loads(data)
            tweet = all_data["text"]
            id = all_data["user"]["id"]
            tim = all_data["created_at"]
            tim = tim.split(" ")
            m = ""


            if tim[1] == "Jan":
                m = "01"
            elif tim[1] == "Feb":
                m = "02"
            elif tim[1] == "Mar":
                m = "03"
            elif tim[1] == "Apr":
                m = "04"
            elif tim[1] == "May":
                m = "05"
            elif tim[1] == "Jun":
                m = "06"
            elif tim[1] == "Jul":
                m = "07"
            elif tim[1] == "Aug":
                m = "08"
            elif tim[1] == "Sep":
                m = "09"
            elif tim[1] == "Oct":
                m = "10"
            elif tim[1] == "Nov":
                m = "11"
            elif tim[1] == "Dec":
                m = "12"
            d = tim[2]
            y = tim[5]
            tim1 = y + "-" + m + "-" + d
            print(tim1)
            usid=1
            usid = all_data["user"]["id"]
            username = all_data["user"]["screen_name"]
            if val != '0':
                cursor.execute(
                    "INSERT INTO twitterdata(id,time, username, tweet,label,keyword,usid) VALUES (%s,%s,%s,%s,NULL,%s,%s)",
                    (self.counter, tim1, username, tweet, val, usid))
            else:
                cursor.execute(
                    "INSERT INTO twitterdata(id,time, username, tweet,label,keyword, usid) VALUES (%s,%s,%s,%s,NULL,NULL,%s)",
                    (self.counter, str(datetime.today()).split(" ")[0], username, tweet,usid))
            connection.commit()
            print(username)
            print(tweet)

            self.counter += 1
            if self.counter < self.limit:
                return True
            else:
                twitterStream.disconnect()

        def on_error(self, status):
            print(status)



    test_tweets = pd.read_csv('..\Firstcode\static\\testing.csv')
    train_tweets = pd.read_csv('..\Firstcode\static\\training.csv')

    # Twitter Trends
    trends1 = apl.trends_place(1)
    data = trends1[0]
    trends = data['trends']
    names = [trend['name'] for trend in trends]
    name = names[:10]
    cursor.execute("SELECT COUNT(*) FROM twittertrends")
    trendcount=cursor.fetchall()[0][0]
    print(trendcount)
    if trendcount==0:
        cursor.execute("INSERT INTO twittertrends(id) VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)")
    for i in range(len(name)):
        cursor.execute("UPDATE twittertrends SET trend=(%s) WHERE id=(%s)",
                       (name[i], i + 1))

    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer

    val=keyword
    uife = [val]

    if val != '0':
        twitterStream = Stream(auth, listener(), timeout=5)
        twitterStream.filter(track=uife)
    else:
        twitterStream = Stream(auth, listener())
        twitterStream.filter(locations=[-180, -90, 180, 90])

    rowcount1 = [0, 0, 0, 0, 0]
    newrowcount1 = [0, 0, 0, 0, 0]

    if val != '0':
        for h in range(5):
            cursor.execute("SELECT COUNT(*) FROM olddata")
            rowcount1[h] = cursor.fetchone()[0]

            count = rowcount1[h]
            cursor.execute("SELECT COUNT(*) FROM olddata")
            rowcount1t = cursor.fetchone()[0]
            count = rowcount1t
            limit = count + 25
            for tweet in tweepy.Cursor(apl.search, q=uife,
                                       since=str(datetime.today() - timedelta(days=h)).split(" ")[0],
                                       until=str(datetime.today() - timedelta(days=h - 1)).split(" ")[0],
                                       lang="en").items():
                count = count + 1
                if count > limit:
                    break
                username = tweet.user.screen_name
                text = tweet.text
                time = str(tweet.created_at).split(" ")[0]
                cursor.execute(
                    "INSERT INTO olddata(id,time, username, tweet,label,keyword) VALUES (%s,%s,%s,%s,NULL,%s)",
                    (count, time, username, text, val))
                connection.commit()
                print(time)
                print(username)
                print(text)
            cursor.execute("SELECT COUNT(*) FROM olddata")
            newrowcount1[h] = cursor.fetchone()[0]

    print(rowcount1)
    print(newrowcount1)
    msg_train, msg_test, label_train, label_test = train_test_split(train_tweets['tweet'], train_tweets['label'],
                                                                    test_size=0.2)

    pipeline = Pipeline([
        ('bow', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB()),
    ])
    pipeline.fit(msg_train, label_train)
    predictions = pipeline.predict(msg_test)
    print("Predictions, classification report, confusion matrix and accuracy score from the testing model.")
    print(predictions)
    print(classification_report(predictions, label_test))
    print(confusion_matrix(predictions, label_test))
    print(accuracy_score(predictions, label_test))
    res=[]
    res1=[]
    cursor.execute("SELECT tweet FROM twitterdata")
    results = cursor.fetchall()
    res = [item[0] for item in results]
    print(res)

    cursor.execute("SELECT tweet FROM olddata")
    results1 = cursor.fetchall()
    res1 = [item[0] for item in results1]
    print(res1)

    print("Prediction of live tweets")
    predictions = pipeline.predict(res)
    prob = pipeline.predict_proba(res)
    print(prob)
    print(predictions)
    cursor.execute("SELECT COUNT(*) FROM twitterdata")
    newrowcount = cursor.fetchone()[0]
    print(newrowcount)
    ncount = 0
    tcount = 0
    for i in range(rowcount, newrowcount):
        if predictions[i] == 0:
            cursor.execute("UPDATE twitterdata set label=\"Not a troll tweet.\" where id=" + str(i) + "")
            connection.commit()
            ncount = ncount + 1
        else:
            cursor.execute("UPDATE twitterdata set label=\"Troll tweet Detected.\" where id=" + str(i) + "")
            connection.commit()
            tcount = tcount + 1

    import matplotlib.pyplot as plt
    labels = 'Not a Troll', 'Troll'
    sizes = [ncount, tcount]
    colors = ['green', '#ee0000']
    plt.pie(sizes, labels= labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Pie Chart')
    plt.savefig("..\Firstcode\static\images\img1.png", format='png', bbox_inches='tight')
    plt.clf()
    plt.close()
    if val!='0':
        print("Prediction of previous tweets")
        predictions1 = pipeline.predict(res1)
        print(predictions1)

        ncount1 = [0.00, 0.00, 0.00, 0.00, 0.00]
        tcount1 = [0.00, 0.00, 0.00, 0.00, 0.00]
        sum1 = [0.00, 0.00, 0.00, 0.00, 0.00]
        ratio1 = [0.00, 0.00, 0.00, 0.00, 0.00]
        for h in range(5):
            for i in range(rowcount1[h], newrowcount1[h]):
                if predictions1[i] == 0:
                    cursor.execute("UPDATE olddata set label=\"Not a troll tweet.\" where id=" + str(i) + "")
                    connection.commit()
                    ncount1[h] = ncount1[h] + 1
                else:
                    cursor.execute("UPDATE olddata set label=\"Troll tweet Detected.\" where id=" + str(i) + "")
                    connection.commit()
                    tcount1[h] = tcount1[h] + 1
            sum1[h] = ncount1[h] + tcount1[h]
            ratio1[h] = float(tcount1[h] / sum1[h])
            print(ratio1[h] * 100)
    sum = ncount + tcount
    ratio = float(tcount / sum)
    print(ratio * 100)
    if val!='0':
        objects = ('Today', 'Yesterday', '2 days ago', '3 days ago', '4 days ago', '5 days ago')
        y_pos = np.arange(len(objects))
        performance = [ratio * 100, ratio1[0] * 100, ratio1[1] * 100, ratio1[2] * 100, ratio1[3] * 100, ratio1[4] * 100]

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Intensity of trolls')
        plt.xlabel('Days')
        plt.title('Bar Graph')
        plt.savefig("..\Firstcode\static\images\img2.png", format='png', bbox_inches='tight')


        plt.close()
        print(prob[rowcount:newrowcount])
        troll_sentiment = []
        troll_sentiment1 = []
        troll_sentiment = prob[rowcount:newrowcount]
        troll_sentiment1 = prob[rowcount:newrowcount]
        troll_sentiment = map(str, troll_sentiment)
        troll_sentiment1 = map(str, troll_sentiment1)
        not_troll = [i.split(' ', 1)[0] for i in troll_sentiment]
        not_troll = [i.strip('[') for i in not_troll]
        for i in range(0, len(not_troll)):
            not_troll[i] = float(not_troll[i]) * 100
        troll = [i.split(' ', 1)[1] for i in troll_sentiment1]
        troll = [i.strip(']') for i in troll]
        for i in range(0, len(troll)):
            troll[i] = float(troll[i]) * 100
        print(not_troll)
        print(troll)
        range_tweets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.scatter(range_tweets, troll, color='b')
        ax.set_xlabel('Number of tweets')
        ax.set_ylabel('Troll Polarity')
        ax.set_title('Scatter plot')
        plt.savefig("..\Firstcode\static\images\img3.png", format='png', bbox_inches='tight')
        plt.close()


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'twitteranalysis'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM twitterdata")
newrowcount = cursor.fetchone()[0]
print(newrowcount)



@app.route('/hello', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        var = '0'
        print(var)
        search(var)
        cursor.execute("SELECT COUNT(*) FROM twitterdata")
        newrowcount = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM twitterdata where id between ' + str(rowcount) + ' and ' + str(newrowcount) + '')
        print(rowcount)
        print(newrowcount)
        data = cursor.fetchall()
        print(data)
        return redirect(url_for('generic'))
    return render_template('hello.html')

@app.route('/individual', methods=['GET', 'POST'])
def individual():
    if request.method == 'POST':
        var = request.form['keyword']
        print(var)
        search(var)
        return redirect(url_for('list'))
    return render_template('individual.html', error=None)

@app.route('/list', methods=['POST', 'GET'])
def list():
    error = None
    data = []
    cursor.execute("SELECT COUNT(*) FROM twitterdata")
    newrowcount = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM twitterdata where id between ' + str(rowcount) + ' and ' + str(newrowcount) + '')
    print(rowcount)
    print(newrowcount)
    data = cursor.fetchall()
    print(data)
    cursor.execute("SELECT * FROM twittertrends")
    data1 = cursor.fetchall()
    if request.method=="post":
        return redirect(url_for('download'))
    return render_template('list.html', error=error, output_data=data, output=data1)

@app.route('/download', methods=['POST', 'GET'])
def download():
    error = None
    data = []
    cursor.execute("SELECT COUNT(*) FROM twitterdata")
    newrowcount = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM twitterdata where id between ' + str(rowcount) + ' and ' + str(newrowcount) + '')
    print(rowcount)
    print(newrowcount)
    data = cursor.fetchall()
    print(data)
    cursor.execute("SELECT * FROM twittertrends")
    data1 = cursor.fetchall()
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    rendered=render_template('list.html',error=error, output_data=data, output=data1)
    pdf=pdfkit.from_string(rendered,False,configuration=config)

    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=output.pdf'
    return response

@app.route('/download1', methods=['POST', 'GET'])
def download1():
    error = None
    data = []
    cursor.execute("SELECT COUNT(*) FROM twitterdata")
    newrowcount = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM twitterdata where id between ' + str(rowcount) + ' and ' + str(newrowcount) + '')
    print(rowcount)
    print(newrowcount)
    data = cursor.fetchall()
    print(data)
    cursor.execute("SELECT * FROM twittertrends")
    data1 = cursor.fetchall()
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    rendered=render_template('generic.html',error=error, output_data=data, output=data1)
    pdf=pdfkit.from_string(rendered,False,configuration=config)

    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=output.pdf'
    return response

@app.route('/report_this/<int:id>', methods=['POST', 'GET'])
def report_this(id=id):
    print("Reporting id : "+str(id))
    apl.report_spam(id)
    return redirect(url_for('list'))

@app.route('/report_this1/<int:id>', methods=['POST', 'GET'])
def report_this1(id=id):
    print("Reporting id : "+str(id))
    apl.report_spam(id)
    return redirect(url_for('generic'))

@app.route('/generic', methods=['POST', 'GET'])
def generic():
    error = None
    data = []
    cursor.execute("SELECT COUNT(*) FROM twitterdata")
    newrowcount = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM twitterdata where id between ' + str(rowcount) + ' and ' + str(newrowcount) + '')
    print(rowcount)
    print(newrowcount)
    data = cursor.fetchall()
    print(data)
    cursor.execute("SELECT * FROM twittertrends")
    data1 = cursor.fetchall()
    if request.method == "post":
        return redirect(url_for('download1'))
    return render_template('generic.html', error=error, output_data=data, output=data1)
    #cur.execute('SELECT * FROM twitterdata where id between '+str(rowcount)+' and '+str(newrowcount)+'')
    #data = cur.fetchall()
    #return render_template('list.html', output_data=data)

@app.route('/indi', methods=['POST', 'GET'])
def indi():
    return render_template('indi.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        flag=1
        username = []
        password = []

        cur.execute("SELECT username from login_table")
        userc = cur.fetchall()

        for t in userc:
            for x in t:
                username.append(x)

        cur.execute("SELECT password from login_table")
        passc = cur.fetchall()

        for t in passc:
            for x in t:
                password.append(x)

        num = []
        cur.execute("SELECT count(*) from login_table")
        numb = cur.fetchone()

        num = int(''.join(map(str, numb)))
        for i in range(num):
            if request.form['username'] == username[i] and request.form['password'] == password[i]:
                flag=0
                break
            else:
                flag=1
        if flag==0:
            return redirect(url_for('hello'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = []
        password = []
        flag = 1
        cur.execute("SELECT username from login_table")
        userc = cur.fetchall()

        for t in userc:
            for x in t:
                username.append(x)

        cur.execute("SELECT password from login_table")
        passc = cur.fetchall()

        for t in passc:
            for x in t:
                password.append(x)

        num = []
        cur.execute("SELECT count(*) from login_table")
        numb = cur.fetchone()

        num = int(''.join(map(str, numb)))
        for i in range(num):
            if request.form['username'] == username[i]:
                flag=0
                break
            else:
                flag=1
        if flag==0:
            error = 'User with this username already has a account'
        else:
            cur.execute("INSERT INTO login_table values(%s,%s)",(request.form['username'],request.form['password']))
            conn.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)