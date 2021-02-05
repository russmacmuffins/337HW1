from json_reader import get_tweets, get_contains, get_most_common
import nltk

tweets = get_tweets('gg2013.json')




def get_award_winner(tweets, award):
    relevant = get_contains(tweets," won ")
    relevant = get_contains(relevant," best ")
    award = nltk.word_tokenize(award)
    for a in award:
        relevant = get_contains(relevant, a)
    return relevant

award = "musical comedy"
r = get_award_winner(tweets, award)

winner = get_most_common(r,1, award)
print(winner)
1+1