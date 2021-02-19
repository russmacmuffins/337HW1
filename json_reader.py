import json
import nltk
import string

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


def filter_awards(award_set):
    filtered = []
    for award in award_set:
        new_award = []
        for w in award.split():
            if w not in stop_words and w not in remove_words:
                new_award.append(w.translate(str.maketrans('', '', string.punctuation)))
        filtered.append(new_award)
    return filtered


filtered_1315 = filter_awards(OFFICIAL_AWARDS_1315)


# print(filtered_1315)

def get_tweets(pathname):
    tweets = []
    try: 
        with open(pathname, 'r') as f:
            data = json.load(f)
        
        for i in range(len(data)):
            t = data[i]['text']
            tweets.append(t.lower())  # all the tweets are all-lowercase
    except IOError:
        print("File %s not found." % pathname)

    return tweets


tweets = get_tweets('gg2013.json')
tweets15 = get_tweets('gg2015.json')


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
def most_common_name(tweetset, award):
    d = {}
    d2 = {}
    banned = ['best', 'wins', 'golden globes', 'golden', 'globes', 'globe', 'goldenglobes']
    award_lst = award.split()
    for a in award_lst:
        banned.append(a)

    ############# set up tweet set
    tweets = tweetset

    if "best" not in award:  # for things like cecil b. demille and other non "best" awards
        tweets = get_contains(tweetset, "wins", "award")
        tweets2 = get_contains(tweetset, "goes to", "award")
    else:
        tweets = get_contains(tweetset, "wins", "best")
        tweets2 = get_contains(tweetset, "goes to", "best")

    ############ determine if we're looking for a person's name
    person = False
    if any(job in award for job in ("actor", "actress", "director")):
        person = True

    ########### get popular phrases and count their occurrence
    def phrase_from_index(find, narrowed_tweets, before, dict):
        for i in range(len(narrowed_tweets)):
            t = narrowed_tweets[i].lower().split()  # nltk.word_tokenize(tweets[i])
            if find not in t:  # for some reason (probably punctuation), this is necessary
                continue
            if "rt" in t:  # remove retweets -- they're not very informative, and they end up tallying higher than informative ones
                continue  # i could see these being more useful when there are fewer tweets to choose from, though

            i = t.index(find)
            if before:
                name = t[:i]  # find the words before "wins"
            else:
                name = t[i+2:]  # find the words after "goes to"
            for w in name:
                #if person:  # no stopwords in people's names, but they are allowed in movie names etc ("THE shape OF water")
                 #   if w in banned or len(
                  #          w) < 2 or w in stop_words:  # unfortunately for don cheadle, "don" is a stopword. Rip
                   #     name.remove(w)
                #else:
                if w in banned or len(w) < 2:
                    name.remove(w)
            ############ convert to string and add to dict counter
            name_string = ' '.join([str(elem) for elem in name])
            name_string = name_string.translate(str.maketrans('', '', string.punctuation))
            # people's names can have punctuation (', -, etc) but movies probably shouldn't
            if name_string in dict:  
                dict[name_string] = dict[name_string] + 1
            else:
                dict[name_string] = 1

    phrase_from_index("wins", tweets, True, d)
    phrase_from_index("goes", tweets2, False, d2)

    def most_common(dict):
        mx = -1
        mx_key = None
        for key in dict:
            if dict[key] > mx:
                mx_key = key
                mx = dict[key]
        return mx_key

    top1 = most_common(d)
    top2 = most_common(d2)
    if top1 and top2:
        common_substring = lcs(top1, top2)  # top1 if d[top1] >= d2[top2] else top2
        if common_substring and len(common_substring)==1:
            winner = ''.join(common_substring)
        else:
            winner = top1 if d[top1] >= d2[top2] else top2  # if it's a tie, go to the answer before "wins" 
    elif not top1 and not top2:
        winner = ' '
    else:
        winner = top1 if top1 else top2
    return winner

def lcs(S,T):  # credit for this function: https://www.bogotobogo.com/python/python_longest_common_substring_lcs_algorithm_generalized_suffix_tree.php
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set

def most_common_host(tweets, award):
    d = {}
    banned = ['best', 'wins', 'GoldenGlobes', 'Golden', 'Globes', 'Globe', 'goldenglobes']
    for a in award:
        banned.append(a)

    for i in range(len(tweets)):
        t = tweets[i].lower().split()  # nltk.word_tokenize(tweets[i])
        if "hosting" not in t:  # for some reason (probably punctuation), this is necessary
            continue
        if t[0] == "rt":  # remove retweets -- they're not very informative, and they end up tallying higher than informative ones
            continue  # i could see these being more useful when there are fewer tweets to choose from, though

        i = t.index("hosting")
        name = t[:i]  # find the words before "hosting"
        for w in name:
            if w == 'and': continue
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
    elif 'and' in host_name:
        name_lst = [x.strip() for x in host_name.split('and')]
    else:
        name_lst.append(host_name)
    return name_lst


# print(get_host(tweets))

def intersect(lst1, lst2):  # using sets would be faster, but we can't because they remove duplicates
    lst3 = [t for t in lst1 if t in lst2]
    return lst3


# gwins = get_contains(tweets, "wins")
gbest = get_contains(tweets, "wins",
                     "best")  # the cecille b demille award doesnt have "best" in it and this is leading to problems
gdirector = get_contains(gbest, "director", None)
gnominated = get_contains(tweets, "nominated", "best")


def filter_tweets_by_award(award,
                           tweetset):  # this function narrows down the tweet set to relevant tweets based on award names
    award_tweets = tweetset
    for i, keyword in enumerate(award):
        if keyword == "motion" and len(award) > i + 1:
            if award[i + 1] == "picture":
                continue
        if keyword == "picture" and i > 0:
            if award[i - 1] == "motion":
                picture = get_contains(award_tweets, "picture",
                                       None)  # no "motion" here because i think "best picture" is a likely phrase
                movie = get_contains(award_tweets, "movie", None)
                film = get_contains(award_tweets, "film", None)
                mp = get_contains(award_tweets, "motion pic", None)  
                award_tweets = movie + film + picture + mp

        if keyword == "series" and len(award) > i + 1:
            if award[
                i + 1] == "miniseries":  # v few tweets will include both series and miniseries, so if miniseries is in the award, add both options
                continue
        if keyword == "miniseries" and i > 0:
            s1 = None
            if award[i - 1] == "series":
                s1 = get_contains(award_tweets, "series", None)
            m1 = get_contains(award_tweets, "miniseries", None)
            m2 = get_contains(award_tweets, "mini series", None)
            m3 = get_contains(award_tweets, "mini-series", None)
            award_tweets = m1 + m2 + m3 if not s1 else m1 + m2 + m3 + s1

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

    for i, award in enumerate(filtered_award_list):
        winner = most_common_name(filter_tweets_by_award(filtered_award_list[i], tweetset), award_list[i])
        winners[award_list[i]] = winner if winner else ' '
       # print(filtered_award_list[i])
        #print(winners[award_list[i]])
    
    return winners


#winner_names_from_awards(OFFICIAL_AWARDS_1315, tweets)

#winner_names_from_awards(OFFICIAL_AWARDS_1315, tweets15)


# print(winner_names_from_awards(OFFICIAL_AWARDS_1315, tweets))

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


# all_nominees()


# strategy to work on:
# get candidate answers word by word: affleck + ben affleck + etc etc
# get the most common candidate across all tweets


1 + 1