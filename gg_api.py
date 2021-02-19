from json_reader import *
from award_reader import awards_get
from pprint import pprint
from nominator import *
from dressed import *
'''Version 0.3'''
import json

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

tweets_by_year = {}
def get_tweet_from_year(year): 
    if year not in tweets_by_year:
        tweets_by_year[year] = get_tweets("gg" + year + ".json")
    return tweets_by_year[year]

def get_answers(year):
    with open('gg%sanswers.json'%year, 'r') as f:
        fres = json.load(f)
    return fres

def get_best_dressed(year):
    tweets = get_tweets_caps("gg" + year + ".json")
    best_worst = best_dressed(tweets)
    best, worst = best_worst
    return best, worst
# print(get_best_dressed("2015"))

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    tweets = get_tweet_from_year(year)

    hosts = get_host(tweets)
    return hosts
# print(get_hosts('2013'))

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    tweets = get_tweet_from_year(year)
    awards = awards_get(tweets)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    tweets2 = get_tweets_caps("gg" + year + ".json")
    nominees = get_nom(tweets2, OFFICIAL_AWARDS)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    #fres = get_answers(year)
    tweets = get_tweet_from_year(year)
    winners = winner_names_from_awards(OFFICIAL_AWARDS, tweets)
    # {award: fres['award_data'][award]['winner'] for award in OFFICIAL_AWARDS}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    fres = get_answers(year)
    presenters = {award: fres['award_data'][award]['presenters'] for award in OFFICIAL_AWARDS}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # f = open("human_readable_answers.txt", "w")
    overall = ["hosts", "awards"]
    specific = ["nominees", "presenters", "winner"]
    extras = ["Best Dressed", "Worst Dressed"]
    d = {}
    
    years = {"2013"}#, "2015"}
    new = input("Enter years to check, separated by a space. Ex: 2013 2015\n")
    for y in new.split():
        years.add(y)

    for year in years:
        gg_nominees = get_nominees(year)
        gg_presenters = get_presenters(year)
        gg_winner = get_winner(year)

        print('Awards %s:' % year)

        for cat in overall:
            results = globals()['get_%s' % cat](year)
            pprint('%s: %s' % (cat.title(), ', '.join(results).title()) )
            if isinstance(results, list): 
                d[cat.title()] = [res.title() for res in results]
            else: d[cat.title()] = results.title()
            # f.write( )
        
        best, worst = get_best_dressed(year)
        print("\nBest Dressed: %s" % best)
        print("Worst Dressed: %s" % worst)
        
        for award in OFFICIAL_AWARDS:
            print('\nAward: %s' % award.title())
            d[award.title()] = {}
            person = False
            if any(job in award for job in ("actor", "actress", "director")):
                person = True

            for cat in specific:
                results = locals()['gg_%s' % cat][award]
                if isinstance(results, list): 
                    d[award.title()][cat.title()] = [res.title() for res in results]
                    results = ', '.join(results)
                else: 
                    d[award.title()][cat.title()] = results.title()
                print('%s: %s' % (cat.title(), results.title()) )
                
    # print(json.dumps(d))

    return

if __name__ == '__main__':
    main()
