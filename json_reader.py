import json
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
remove_words = ['-', 'best', 'performance']


filtered_1315 = []
for award in OFFICIAL_AWARDS_1315:
    filtered_award = []
    for w in award.split():
        if w not in stop_words and w not in remove_words:
            filtered_award.append(w)
    filtered_1315.append(filtered_award)
# print(filtered_1315)

def get_tweets(pathname):
    tweets = []
    with open(pathname, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        tweets.append(data[i]['text'])

    tweets = [t.lower() for t in tweets]

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
    banned = ['best', 'wins', 'GoldenGlobes','Golden','Globes','Globe','goldenglobes']
    for a in award:
        banned.append(a)
    for i in range(len(tweets)):
        t = nltk.word_tokenize(tweets[i])
        for w in t:  # changed to 1 because some names (i.e., "Ben" or "Li") are short, and we can use stopwords here
            if len(w) > 1 and w not in stop_words and w not in banned:
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


# in the help session they mentioned just getting the most common strings (any word length),
# because after the actual name the rest of the results would be less common

# award input here will be from the filtered list, and awards are already .split() in that list
def most_common_name(tweets, award):
    d = {}
    banned = ['best', 'wins', 'GoldenGlobes','Golden','Globes','Globe','goldenglobes']
    for a in award:
        banned.append(a)

    for i in range(len(tweets)):
        t = tweets[i].lower().split() # nltk.word_tokenize(tweets[i])
        i = t.index("wins")
        name = t[:i]
        for w in name:
            if w in banned or w in stop_words or len(w) < 2:
                name.remove(w)
        
        name_string = ' '.join([str(elem) for elem in name])
        
        if name_string in d:
            d[name_string] = d[name_string] + 1
        else: 
            d[name_string] = 1
    
    mx = -1
    mx_key = None
    for key in d:
        if d[key] > mx:
            mx_key = key
            mx = d[key]

    return mx_key

gwins = get_contains(tweets,"wins")
gbest = get_contains(gwins,"best")
gdirector = get_contains(gbest,"director")
print(most_common_name(gdirector, OFFICIAL_AWARDS_1315[11]))

def intersect(lst1, lst2):  # using sets would be faster, but we can't because they remove duplicates
    lst3 = [t for t in lst1 if t in lst2]
    return lst3

1+1