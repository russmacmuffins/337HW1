import json
import nltk


def get_tweets(pathname):
    tweets = []
    with open(pathname, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        tweets.append(data[i]['text'])

    return tweets


tweets = get_tweets('gg2013.json')

def tokenize(tweet):
    sentences = nltk.sent_tokenize(tweet)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    #sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def get_contains(tweets, word):
    A = []
    for t in tweets:
        if t.find(word) != -1:
            A.append(t)

    return A

def get_most_common(tweets, num, award):
    award = nltk.word_tokenize(award)
    d = {}
    banned = ['best', 'won', 'GoldenGlobes','Golden','Globes','Globe','goldenglobes']
    for a in award:
        banned.append(a)
    for i in range(len(tweets)):
        t = nltk.word_tokenize(tweets[i])
        for w in t:
            if len(w) > 3 and w not in banned:
                if w in d:
                    d[w] = d[w] + 1
                else:
                    d[w] = 1
    
    mx = -1
    mx_key = None
    for key in d:
        if d[key] > mx:
            mx_key = key
            mx = d[key]

    return mx_key



gwon = get_contains(tweets,"won")
gbest = get_contains(gwon,"best")
gdirector = get_contains(gbest,"director")


1+1