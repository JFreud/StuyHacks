import requests, json, twitter, oauth2, ast, urllib2

NYT_API_KEY = "a7e4cb2fa4bf4516b1ca846478b5db68"
TWITTER_CONSUMER_KEY = "woOeXTL0XV2dO6YQuVLEdx7GP"
TWITTER_CONSUMER_SECRET = "hE1w9Ott1NWjb8OIXlpbhRcyvO54TJt7sIJ8mPYeVXsKvRI2O7"
TWITTER_ACCESS_TOKEN = "1426838582-YkU3XAVMUGXuUAazLdsIFyF5oFE4wpBcbkcq7o3"
TWITTER_ACCESS_SECRET = "oecREA8AiMacla9ROxDKodPxKqy5D4vs2bEmfXWTrIE1G"

def oauth_twitter(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key=TWITTER_ACCESS_TOKEN, secret=TWITTER_ACCESS_SECRET)
    client = oauth2.Client(consumer, token)
    content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content


def get_twitter():
    url = "https://api.twitter.com/1.1/search/tweets.json?q=from:%40realDonaldTrump&result_type=recent"
    content = oauth_twitter(url, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    data = json.loads(content[1])
    return data

#returns dict keyed by article headline and value is a list of [url, snippet, date]
def get_articles():
    watson = run_watson()
    query = urllib2.quote(filter_keys(watson))
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?api_key=%s&q=%s&begin_date=20171001" %(NYT_API_KEY, query)
    r = requests.get(url)
    data = r.text
    articles = json.loads(data)[docs]
    article_list = {}
    for article in articles:
        articleInfo = []
        articleInfo.append(article["web_url"])
        articleInfo.append(article["snippet"])
        articleInfo.append(article["pub_date"])
        article_list[article["headline"]["main"]] = articleInfo
    return article_list


if __name__ == "__main__":
    statuses = get_twitter()['statuses']
    for status in statuses:
        print(status['entities']['urls'])

