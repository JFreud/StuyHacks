import requests, json

NYT_API_KEY = "a7e4cb2fa4bf4516b1ca846478b5db68"
TWITTER_API_KEY = ""





















































































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

