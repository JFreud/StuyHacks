from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import api
import requests,json

my_app = Flask (__name__)

@my_app.route('/')
def root():
    tweets = api.get_trump_urls()
    tweet_text = api.get_trump_texts()
    return render_template('home.html',tweets = tweets, tweet_text = tweet_text)

@my_app.route('/analyze')
def analyze():
    tweet = request.args.get('tweet_text')
    article_list = api.get_articles(tweet)
    return article_list

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
