from json_reader import tokenize, get_tweets, get_contains, get_most_common, most_common_name
#from award_reader import remove_banned
import nltk

tweets = get_tweets('gg2013.json')




""" def get_award_winner(tweets, award):
    relevant = get_contains(tweets," won ")
    relevant = get_contains(relevant," best ")
    award = nltk.word_tokenize(award)
    for a in award:
        relevant = get_contains(relevant, a)
    return relevant

award = "musical comedy"
r = get_award_winner(tweets, award)

winner = get_most_common(r,1, award)
print(winner) """


def get_hosts(tweets):
    for t in tweets:
        t = tokenize(tweets)
    relevent = get_contains(tweets, "hosts", "and")
    host_names = get_most_common(relevent, 1, "hosts")
    #host_names = most_common_name(relevent, "hosts")
    #remove_banned(relevent, host_names)
    # i want to find the two most common names in the tweets that include 'host', or 'hosted by'
    # two names or one? sometimes one host, sometimes two
    # find most common name (how to get first and last?), then make the get_most_common ignore that name?
    # ban that name, then run it again to find the second most common name?
    #for t in tweets:

    host_names+=(get_most_common(relevent, 1, host_names))
    print("hosts here:")
    print(host_names)
    return host_names

get_hosts(tweets)

1+1