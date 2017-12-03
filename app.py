from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import api
import requests,json,time

my_app = Flask (__name__)

@my_app.route('/')
def root():
    urls = api.get_trump_urls()
    texts = api.get_trump_texts()
    return render_template('home.html', urls = urls, texts = texts, get_articles = api.get_articles, sleep = time.sleep)


@my_app.route('/article', methods = ["GET"])
def article():
    tweet = request.args["tweet"]
    return render_template('article.html', get_articles = api.get_articles, sleep = time.sleep, tweet = tweet)

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
