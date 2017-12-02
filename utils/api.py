import requests, json, twitter, oauth2, ast, urllib2
from requests.auth import HTTPBasicAuth

NYT_API_KEY = "a7e4cb2fa4bf4516b1ca846478b5db68"
TWITTER_CONSUMER_KEY = "woOeXTL0XV2dO6YQuVLEdx7GP"
TWITTER_CONSUMER_SECRET = "hE1w9Ott1NWjb8OIXlpbhRcyvO54TJt7sIJ8mPYeVXsKvRI2O7"
TWITTER_ACCESS_TOKEN = "1426838582-YkU3XAVMUGXuUAazLdsIFyF5oFE4wpBcbkcq7o3"
TWITTER_ACCESS_SECRET = "oecREA8AiMacla9ROxDKodPxKqy5D4vs2bEmfXWTrIE1G"

IBM_USER = "ba0b75ff-9d1a-46b4-abfb-cb44113a2449"
IBM_PASS= "CdnsqCmfLbns"

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      elif isinstance(d[key],list):
         print "["
         for item in d[key]:
            pretty(item, indent+2)
         print "]"
      else:
         print('\t' * (indent+1) + str(value))


#--------------------WATSON ----------------------------------
def run_watson(tweet):

    encoded_tweet = urllib2.quote(tweet)

    link =  'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2017-02-27&text=' + encoded_tweet + "&features=keywords"

    results = requests.get(link, auth=HTTPBasicAuth(IBM_USER,IBM_PASS))

    #results is now a dictionary
    results = results.json()

    print pretty(results)
    return results


def filters_keys(keyword_dict):
    keyword_dict = keyword_dict["keywords"]
    keywords = []
    keywords.append(keyword_dict[0]["text"])

    for item in keyword_dict :
        #print "DDDDD: " + item["text"]
        if len(keywords) ==3:
            return keywords

        counter = 0
        repeated = False

        for word in keywords:
            word_list1 = word.split(" ")
            #print word_list1
            for i in word_list1:
               if i in item["text"]:
                  repeated = True
            #print repeated


            if item["text"] in word or repeated:
                #print "SDFFFFFFFFFFFFF"
                break
            else:
                counter +=1

        if counter == len(keywords):
            #print item["text"]
            keywords.append(item["text"])

    stringed_keywords = (" ").join(keywords)

#------------------------------------------------------------

#------------------------------TWITTER----------------------------

def oauth_twitter(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key=TWITTER_ACCESS_TOKEN, secret=TWITTER_ACCESS_SECRET)
    client = oauth2.Client(consumer, token)
    content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content



def get_trump_urls():
    url = "https://api.twitter.com/1.1/search/tweets.json?q=from:%40realDonaldTrump&result_type=recent"
    content = oauth_twitter(url, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    statuses = json.loads(content[1])['statuses']
    # print statuses[0]['full_text']
    # print statuses[1]['full_text']
    # print "\n\n\n ^statuses \n\n\n\n"
    url_list = []
    for status in statuses:
        url_list.append(status['entities']['urls'])
    return url_list

def get_trump_texts():
    url = "https://api.twitter.com/1.1/search/tweets.json?q=from:%40realDonaldTrump&result_type=recent&tweet_mode=extended"
    content = oauth_twitter(url, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    statuses = json.loads(content[1])['statuses']
    text_list = []
    for status in statuses:
        # print "status:\n\n\n\n"
        # print status
        try:
            text_list.append(status['full_text'])
        except KeyError:
            pass
    return text_list

#------------------------------------------------------------

#------------------------------NYT------------------------------

#returns dict keyed by article headline and value is a list of [url, snippet, date]
#returns a list of lists with a list for each article [headline, url, snippet, date]
def get_articles(tweet):
    watson = run_watson(tweet)
    query = urllib2.quote(filter_keys(watson))
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?api_key=%s&q=%s&begin_date=20171001" %(NYT_API_KEY, query)
    r = requests.get(url)
    data = r.text
    articles = json.loads(data)[docs]
    article_list = []
    for article in articles:
        articleInfo = []
        articleInfo.append(article["headline"]["main"])
        articleInfo.append(article["web_url"])
        articleInfo.append(article["snippet"])
        articleInfo.append(article["pub_date"])
        article_list.append(articleInfo)
    return article_list


#-----------------------------------------------------------------

if __name__ == "__main__":
    trump_urls = get_trump_urls()
    print trump_urls
    print "\n\n==============\n\n"
    trump_texts = get_trump_texts()
    for tweet in trump_texts:
        print get_articles(tweet)
