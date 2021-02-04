import json



def get_tweets(pathname):
    tweets = []
    with open(pathname, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        tweets.append(data[i]['text'])

    return tweets


tweets = get_tweets('gg2013.json')


def get_contains(tweets, word):
    A = []
    for t in tweets:
        if t.find(word) != -1:
            A.append(t)

    return A

g = get_contains(tweets,"won")

1+1