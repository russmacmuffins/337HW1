from json_reader import get_tweets, get_contains, get_most_common
from award_reader import remove_banned
import nltk
import json
from nominator import get_tweets_caps
nltk.download('averaged_perceptron_tagger')

def find_look(words):
  for i in range(len(words)):
    if words[i][0] == "looks":
      return i;


def get_person(tweet):
  split = nltk.word_tokenize(tweet)
  split = nltk.pos_tag(split)
  start = False
  anchor = find_look(split)
  name = ""
  for i in range(anchor, -1, -1):
    if split[i][1] == "NNP" and split[i][0] != "@":
      name = split[i][0] + " " + name
      start = True
    elif start:
      return name
  return "None"
      

def get_intent(tweet):
  positive_bank = set(["great", "good", "sexy", "amazing", "stunning", "fine", "gorgeous", "GOOD", "nice", "fantastic"])
  negative_bank = set(["terrible", "bad", "ugly", "sad", "uncomfortable", "messy"])
  split = nltk.word_tokenize(tweet)
  split = nltk.pos_tag(split)
  anchor = find_look(split)
  for i in range(anchor, len(split)):
    if split[i][1] == "JJ":
      if split[i][0] in positive_bank:
        return 1
      elif split[i][0] in negative_bank:
        return -1
      else:
        return 0
  return 0

def best_dressed(tweets):
  imp = []
  relevant = get_contains(tweets," looks ", "goldenglobes")
  imp.extend(relevant)
  fin = {}
  for i in imp:
    if get_person(i) in fin:
      fin[get_person(i)] += get_intent(i)
    else:
      fin[get_person(i)] = get_intent(i)
  sorter = sorted(fin, key=fin.get, reverse=True)
  for i in range(len(sorter) -1, -1, -1):
    if len(sorter[i]) < 4 or sorter[i] == "None":
      sorter.pop(i)
  #print(sorter)
  return (sorter[0], sorter[-1])

