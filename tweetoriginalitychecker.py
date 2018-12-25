from flask import Flask, render_template, url_for, g, redirect, session, flash, request
from functools import wraps
from flaskext.mysql import MySQL
from datetime import datetime
import twitter as twitter_api
from twitter.error import TwitterError
from generateDoc2VecText import generatesimilartext
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)

app.config.from_object('config')

mysql = MySQL()
mysql.init_app(app)

blueprint = make_twitter_blueprint(
    api_key=app.config['TWITTER_CONSUMER_KEY'],
    api_secret=app.config['TWITTER_CONSUMER_SECRET'],
)
app.register_blueprint(blueprint, url_prefix="/login")

api = twitter_api.Api(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
        access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'],
        tweet_mode='extended')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not twitter.authorized:
            return redirect(url_for("twitter.login"))
        return f(*args, **kwargs)
    return decorated_function

def globals(f):
    @wraps(f)
    def global_function(*args, **kwargs):
        cursor = mysql.get_db().cursor()

        if twitter.authorized:
            tw_user = twitter.get("account/verify_credentials.json").json()
            cursor.execute('''SELECT COUNT(*) FROM users WHERE tw_id = %s''', (int(tw_user["id"])))

            if (str(cursor.fetchone()[0]) == '0'):
                cursor.execute(
                    """INSERT INTO users (tw_id, tw_name, tw_screen_name, tw_image, tw_location, tw_created_at)
                    VALUES (%s,%s,%s,%s, %s, %s)""",
                    (int(tw_user["id"]), tw_user["name"], tw_user["screen_name"], tw_user["profile_image_url"],
                     tw_user["location"], datetime.strptime(tw_user["created_at"], "%a %b %d %H:%M:%S %z %Y")))
            else:
                cursor.execute(
                    """UPDATE users SET tw_name=%s, tw_screen_name=%s, tw_image=%s, tw_location=%s
                    WHERE tw_id=%s""",
                    (tw_user["name"], tw_user["screen_name"], tw_user["profile_image_url"], tw_user["location"],
                     int(tw_user["id"])))

            mysql.get_db().commit()

            cursor.execute('''SELECT * FROM users WHERE tw_id = %s''', (int(tw_user["id"])))

            user = cursor.fetchall()[0]

            g.user = {
                "id": user[0],
                "tw_id": user[1],
                "name": user[2],
                "screen_name": user[3],
                "photo": user[4]
            }
        return f(*args, **kwargs)
    return global_function

@app.route('/')
@globals
def welcome():
    return render_template("welcome.html")

@app.route('/logout')
def logout():
    del app.blueprints['twitter'].token
    session.clear()
    flash("See you next time!")

    return redirect(url_for("welcome"))

@app.route('/index')
@login_required
@globals
def index():
    return render_template("index.html")

@app.route('/analysis', methods=['POST'])
@login_required
@globals
def analysis():
    data = request.form['url'].split('/')

    try:
        status = api.GetStatus(int(data[2]))

    except TwitterError as e:
        flash("TwitterError :" + str(e.message))

        return redirect(url_for("index"))

    tweet = {
        "tw_id": int(data[2]),
        "tw_text": str(status.full_text),
        "tw_created_at": datetime.strptime(status.created_at, "%a %b %d %H:%M:%S %z %Y").strftime('%Y-%m-%d %H:%M:%S'),
        "tw_user": {
            "name": status.user.name,
            "screen_name": status.user.screen_name,
            "profile_image_url": status.user.profile_image_url_https
        }
    }

    if str(data[0]) != tweet['tw_user']['screen_name'] or str(data[1]) != 'status':
        flash("Wrong tweet URL!")

        return redirect(url_for("index"))

    try:
        similar_tweet = api.GetSearch(raw_query=
                                      "q="
                                      + tweet['tw_text'].replace(" ", "%20").replace("'", "%27")
                                      + "&until="
                                      + datetime.strptime(tweet['tw_created_at'], "%Y-%m-%d %H:%M:%S")
                                      .strftime('%Y-%m-%d')
                                      + "&count=1&result_type=popular")
    except TwitterError as e:
        similar_tweet = {}

        flash("TwitterError :" + str(e.message))

    generated_sentences = generatesimilartext(tweet['tw_text'])

    return render_template('analysis.html', tweet=tweet, similar_tweet=similar_tweet, generated_sentences=generated_sentences)

if __name__ == '__main__':
    app.run(debug=True)
