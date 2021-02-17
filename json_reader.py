import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best motion picture - comedy or musical',
                        'best performance by an actress in a motion picture - comedy or musical',
                        'best performance by an actor in a motion picture - comedy or musical',
                        'best animated feature film', 'best foreign language film',
                        'best performance by an actress in a supporting role in a motion picture',
                        'best performance by an actor in a supporting role in a motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best original score - motion picture', 'best original song - motion picture',
                        'best television series - drama',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best television series - comedy or musical',
                        'best performance by an actress in a television series - comedy or musical',
                        'best performance by an actor in a television series - comedy or musical',
                        'best mini-series or motion picture made for television',
                        'best performance by an actress in a mini-series or motion picture made for television',
                        'best performance by an actor in a mini-series or motion picture made for television',
                        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best performance by an actress in a motion picture - musical or comedy',
                        'best performance by an actor in a motion picture - musical or comedy',
                        'best performance by an actress in a supporting role in any motion picture',
                        'best performance by an actor in a supporting role in any motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best motion picture - animated', 'best motion picture - foreign language',
                        'best original score - motion picture', 'best original song - motion picture',
                        'best television series - drama', 'best television series - musical or comedy',
                        'best television limited series or motion picture made for television',
                        'best performance by an actress in a limited series or a motion picture made for television',
                        'best performance by an actor in a limited series or a motion picture made for television',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best performance by an actress in a television series - musical or comedy',
                        'best performance by an actor in a television series - musical or comedy',
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
                        'cecil b. demille award']
remove_words = ['-', 'best', 'performance', 'award', 'role', 'made']

'''
filtered_1315_1 = []
for award in OFFICIAL_AWARDS_1315:
    filtered_award = []
    for w in award.split():
        if w not in stop_words and w not in remove_words:
            filtered_award.append(w)
    filtered_1315_1.append(filtered_award)
'''

def filter_awards(award_set):
    filtered = []
    for award in award_set:
        new_award = []
        for w in award.split():
            if w not in stop_words and w not in remove_words:
                new_award.append(w)
        filtered.append(new_award)
    return filtered

filtered_1315 = filter_awards(OFFICIAL_AWARDS_1315)


# print(filtered_1315)

def get_tweets(pathname):
    tweets = []
    with open(pathname, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        t = data[i]['text']
        tweets.append(t.lower())  # all the tweets are all-lowercase

    return tweets


tweets = get_tweets('gg2013.json')


def tokenize(tweet):
    sentences = nltk.sent_tokenize(tweet)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    # sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def get_contains(tweets, word1, word2):  # i added another input, potentially to help with efficiency down the road
    A = []
    for t in tweets:
        if t.find(word1) != -1:
            if word2 and t.find(word2) != -1:  # we have a word2 and it matches
                A.append(t)
            elif not word2:  # we don't have word2
                A.append(t)

    return A


def get_most_common(tweets, num, award):
    award = nltk.word_tokenize(award)
    d = {}
    banned = ['best', 'wins', 'GoldenGlobes', 'Golden', 'Globes', 'Globe', 'goldenglobes']
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
    banned = ['best', 'wins', 'GoldenGlobes', 'Golden', 'Globes', 'Globe', 'goldenglobes']
    for a in award:
        banned.append(a)

    for i in range(len(tweets)):
        t = tweets[i].lower().split()  # nltk.word_tokenize(tweets[i])
        if "wins" not in t:  # for some reason (probably punctuation), this is necessary
            continue
        if t[0] == "rt":  # remove retweets -- they're not very informative, and they end up tallying higher than informative ones
            continue  # i could see these being more useful when there are fewer tweets to choose from, though

        i = t.index("wins")
        name = t[:i]  # find the words before "wins"
        for w in name:
            if w in banned or w in stop_words or len(w) < 2:
                name.remove(w)

        name_string = ' '.join([str(elem) for elem in name])

        if name_string in d:  # ok, from here i want to find a way to get the most common substrings from these most common name strings
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


def most_common_host(tweets, award):
    d = {}
    banned = ['best', 'wins', 'GoldenGlobes', 'Golden', 'Globes', 'Globe', 'goldenglobes']
    for a in award:
        banned.append(a)

    for i in range(len(tweets)):
        t = tweets[i].lower().split()  # nltk.word_tokenize(tweets[i])
        if "hosting" not in t:  # for some reason (probably punctuation), this is necessary
            continue
        if t[
            0] == "rt":  # remove retweets -- they're not very informative, and they end up tallying higher than informative ones
            continue  # i could see these being more useful when there are fewer tweets to choose from, though

        i = t.index("hosting")
        name = t[:i]  # find the words before "hosting"
        for w in name:
            if w in banned or w in stop_words or len(w) < 2:
                name.remove(w)

        name_string = ' '.join([str(elem) for elem in name])

        if name_string in d:  # ok, from here i want to find a way to get the most common substrings from these most common name strings
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


def get_host(tweets):
    # relevant = get_contains(tweets, "hosts", "host")
    relevant2 = get_contains(tweets, "hosting", None)
    # tweet_bank = relevant.extend(relevant2)
    host_name = most_common_host(relevant2, "hosting")

    name_lst = []  # we have to return a list per the autograder 

    # formatting answer to be two strings with no &amp
    if '&amp;' in host_name:
        name_lst = [x.strip() for x in host_name.split('&amp;')]
        # reversing the order of the names, bc was geting 'tina fey' 'amy poehler' but this might not be necessary
        # [S.T.] I am changing this because it's not a given that names are two words
        # name1 = names[3] + ' ' + names[4]
        # name2 = names[0] + ' ' + names[1]
    else:
        name_lst.append(host_name)
    return name_lst


#print(get_host(tweets))

def intersect(lst1, lst2):  # using sets would be faster, but we can't because they remove duplicates
    lst3 = [t for t in lst1 if t in lst2]
    return lst3


# gwins = get_contains(tweets, "wins")
gbest = get_contains(tweets, "wins",
                     "best")  # the cecille b demille award doesnt have "best" in it and this is leading to problems
gdirector = get_contains(gbest, "director", None)
gnominated = get_contains(tweets, "nominated", "best")


def filter_tweets_by_award(award, tweetset):
    award_tweets = tweetset
    for i, keyword in enumerate(award):
        # this is probably not necessary but i wanted to keep these as one phrase in the search
        if keyword == "motion" and len(award) > i + 1:
            if award[i + 1] == "picture":
                continue
        if keyword == "picture" and i > 0:
            if award[i - 1] == "motion":
                picture = get_contains(award_tweets, "picture", None)
                movie = get_contains(award_tweets, "movie", None)
                film = get_contains(award_tweets, "film", None)
                # mp = get_contains(award_tweets, "motion picture", None)
                award_tweets = movie + film + picture

        if keyword == "series" and len(award) > i + 1:
            if award[i + 1] == "mini-series":
                continue
        if keyword == "mini-series" and i > 0:
            m1 = get_contains(award_tweets, "miniseries", None)
            m2 = get_contains(award_tweets, "mini series", None)
            m3 = get_contains(award_tweets, "mini-series", None)
            award_tweets = m1 + m2 + m3

        if keyword == "television":
            TV = get_contains(award_tweets, "tv", None)
            television = get_contains(award_tweets, "television", None)
            award_tweets = TV + television
        else:
            award_tweets = get_contains(award_tweets, keyword, None)
    return award_tweets


def winner_names_from_awards(award_list, tweetset):
    winners = dict.fromkeys(award_list)

    filtered_award_list = filter_awards(award_list)

    tweets_best = get_contains(tweetset, "wins", "best")

    for i, award in enumerate(filtered_award_list):
        winner = most_common_name(filter_tweets_by_award(filtered_award_list[i], tweets_best), award_list[i])
        winners[award_list[i]] = winner if winner else ' '
       # print(filtered_award_list[i])
       # print(most_common_name(filter_tweets_by_award(filtered_award_list[i], gbest), award_list[i]))
        # print(most_common_name(filter_tweets_by_award(filtered_1315[i], gbest), filtered_1315[i]))
    
    return winners


# winner_names_from_awards(OFFICIAL_AWARDS_1315, tweets)

def get_nominees(tweets, award, prev_name):
    # get the most common name before "nominated" and the award
    # add it to the banned list
    # rinse + repeat x5

    d = {}
    banned = ['best', 'wins', 'golden', 'globes', 'globe', 'goldenglobes']  # these need to be lowercase
    banned.append(award)

    for i in range(len(tweets)):
        t = tweets[i].lower().split()  # nltk.word_tokenize(tweets[i])
        if "nominated" not in t:  # for some reason (probably punctuation), this is necessary
            continue
        if t[
            0] == "rt":  # remove retweets -- they're not very informative, and they end up tallying higher than informative ones
            continue  # i could see these being more useful when there are fewer tweets to choose from, though

        i = t.index("nominated")
        name = t[:i]  # find the words before "wins"
        for w in name:
            if w in banned or w in stop_words or len(w) < 2:
                name.remove(w)

        name_string = ' '.join([str(elem) for elem in name])

        if name_string in d:  # ok, from here i want to find a way to get the most common substrings from these most common name strings
            d[name_string] = d[name_string] + 1
        else:
            d[name_string] = 1

    mx = -1
    mx_key = None
    for key in d:
        if d[key] > mx and key not in prev_name:
            mx_key = key
            mx = d[key]

    return mx_key


def nominee_names_from_award(award):
    nominees = []
    for i in range(5):
        tmp = get_nominees(filter_tweets_by_award(award, gnominated), award, nominees)
        nominees.append(tmp)
        # print(nominees)
    return nominees


def all_nominees():
    for i, award in enumerate(filtered_1315):
        print(OFFICIAL_AWARDS_1315[i])
        print(nominee_names_from_award(OFFICIAL_AWARDS_1315[i]))


#all_nominees()


# strategy to work on:
# get candidate answers word by word: affleck + ben affleck + etc etc
# get the most common candidate across all tweets



1 + 1