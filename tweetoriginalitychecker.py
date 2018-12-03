import os
from flask import Flask, request, render_template
import sqlite3
import twitter

app = Flask(__name__)

app.config.from_object('config')

conn = sqlite3.connect('database.db')

api = twitter.Api(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
        access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'],
        tweet_mode='extended')

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/twitterdemo')
def twitterdemo():
    return str(api.GetSearch(term='Trump', result_type='popular', count=1, return_json=True))

@app.route('/test')
def test():
    return "Opened database successfully";

if __name__ == '__main__':
    app.run(debug=True)
