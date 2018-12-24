from flask import Flask
import requests
from flaskext.mysql import MySQL
import twitter as twitter_api

app = Flask(__name__)

app.config.from_object('config')

mysql = MySQL()
mysql.init_app(app)

cursor = mysql.get_db().cursor()

api = twitter_api.Api(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
        access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'],
        tweet_mode='extended')


def test_is_application_up():
    assert requests.head("http://tweetoriginalitychecker.com").status_code == 200


def test_twitter_connection():
    assert len(api.GetSearch(raw_query="q=test")) > 0


def test_mysql_connection():
    assert cursor.execute('''SHOW TABLES''').fetchall() > 0
