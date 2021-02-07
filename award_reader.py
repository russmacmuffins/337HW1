from json_reader import get_tweets, get_contains, get_most_common
import nltk
nltk.download('punkt')
from nltk.collocations import *

tweets = get_tweets('gg2013.json')

#removes all words before the word for (inc)
def clean_awards(awards):
  new = []
  for i in awards:
    if i.find(" rt ") != -1 or i.find(" rt") != -1 or i[0:3] == "rt ": 
      print("removed RT")
      continue
    in1 = i.find(" won golden globe for ")
    in2 = i.find(" nominated for ")
    if (in1 != -1):
      new.append(i[in1 + 22:])
    else:
      new.append(i[in2 + 15:])
  return new
  
def remove_banned(awards, banned):
  for i in range(len(awards)-2, -1, -1):
    for j in banned:
      if (awards[i].find(j) != -1):
        awards.pop(i)
        
def filter_noise(awards):
  new = []
  stop_signal = [".", "#", ",","?", "for"]
  for i in range(len(awards)):
    lowest = 100
    for j in stop_signal:
      temp = awards[i].find(j)
      if (temp < lowest and temp != -1):
        lowest = temp
    new.append(awards[i][:lowest])
  return new


def count_common(awards):
  temp = []
  for i in awards:
    base = i.split()
    temp.extend(base)
  bigram_measures = nltk.collocations.BigramAssocMeasures()
  trigram_measures = nltk.collocations.TrigramAssocMeasures()
  finder = TrigramCollocationFinder.from_words(temp)
  finder.apply_freq_filter(2)
  return finder.nbest(trigram_measures.pmi, 10)


def get_awards(tweets):
    awards = []
    relevant = get_contains(tweets," won golden globe for", "goldenglobes")
    awards.extend(relevant)
    relevant = get_contains(tweets," nominated for ", "goldenglobes")
    awards.extend(relevant)
    awards = clean_awards(awards)
    banned = ["something", "anything", "everything", "oscar", "golden globe", "academy award", "academyaward", "emmy", "awards"]
    remove_banned(awards, banned)
    awards = filter_noise(awards)
    final = count_common(awards)
    print(awards)
    return final


r = get_awards(tweets)

