from json_reader import get_tweets, get_contains, get_most_common
from award_reader import remove_banned
import nltk
import json
nltk.download('averaged_perceptron_tagger')

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



def get_tweets_caps(pathname):
    tweets = []
    with open(pathname, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        t = data[i]['text']
        tweets.append(t)

    return tweets

#tweets = get_tweets_caps("gg2013.json")

def clean_noms(noms):
  new = []
  for i in noms:
    if i.find(" rt ") != -1 or i.find(" rt") != -1 or i[0:3] == "rt ": 
      continue
    new.append(i)
  return new

def crack_sift(award):
  split = nltk.word_tokenize(award)
  split = nltk.pos_tag(split)
  out = []
  for i in split:
    if ((i[1] == 'NN' or i[1] == 'NNP') and i[0] != 'performance' and i[0] != 'role' and i[0] != 'motion' and i[0] != 'picture' and i[0] != 'series'):
      out.append(i[0])
          #print(out)
  return out

def findBanned(string):
  banned = ["golden", "globes", "score", "actor", "actress"]
  if (string[1:] == ''):
    return False
  for i in banned:
    if (string.find(i) != -1):
      return False
  return True

def refilter(loStr):
  for i in range(len(loStr) - 1, -1, -1):
      if len(loStr[i]) < 5 or loStr[i].find("olden") != -1 or loStr[i].find("lobes") != -1:
        loStr.pop(i)


def get_actor_noms(usable):
  out = {}
  #print(usable)
  tip = type(0)
  for i in usable:
    split = nltk.word_tokenize(i)
    split = nltk.pos_tag(split)
    cont = 0
    current = ""
    for j in split:
      if (j[0] == "RT"):
        cont = -2
      elif ((j[0] == "@") or (j[0] == "#")):
            if(findBanned(j[0])):
                if j[0] in out:
                    out[j[0][1:]] += 1
                else:
                    out[j[0][1:]] = 0
                current = ""
      elif (cont < 0):
        cont += 1
      elif ((cont >= 1 and j[1] != "NNP") and findBanned(current)):
        if current in out:
          out[current] += 1
        else:
          out[current] = 0
        current = ""
      elif (j[1] == "NNP"):
        cont += 1
        current = current + " " + j[0]
      else:
        current = ""
        cont = 0
  sorter = sorted(out, key=out.get, reverse=True)
  refilter(sorter)
#print(sorter[:5])
  return sorter[:5]

def get_film_noms(usable, keys):
  out = {}
  seg_bank = {" - ", ":", "goes to", ", ", " (", "!", "#"}
  for i in usable:
    split = nltk.word_tokenize(i)
    short_term = ""
    switch = True
    for j in split:
      if (j in seg_bank) and not(switch):
        switch = True
      elif switch and not(j in keys):
        short_term += j
      elif switch and (j in keys):
        switch = False







def get_award_noms(award, tweets):
  keys = crack_sift(award)
  usable = []
  isactor = False
  for i in tweets:
    boll = True
    for j in keys:
      if (i.find(j) == -1):
        boll = False
      if (j == 'actor' or j == 'actress'):
        isactor = True
    if boll:
      usable.append(i)
  return get_actor_noms(usable)
    
    


def get_nom(tweets, awards):
  noms = []
  relevant = get_contains(tweets," nom", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," should have", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," lost", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," hope", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," snubbed", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," hoping", "goldenglobes")
  noms.extend(relevant)
  relevant = get_contains(tweets," rooting for", "goldenglobes")
  noms.extend(relevant)
  final = {}
  for i in awards:
    temp = get_award_noms(i, noms)
    final[i] = temp
  # print(final)
  return final


#get_nom(tweets, OFFICIAL_AWARDS_1315)
