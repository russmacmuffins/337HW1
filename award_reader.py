from json_reader import get_tweets, get_contains, get_most_common
import nltk
from nltk.collocations import *
from nltk import ngrams

#removes all words before the word for (inc)
def clean_awards(awards):
  new = []
  for i in awards:
    if i.find(" rt ") != -1 or i.find(" rt") != -1 or i[0:3] == "rt ": 
      continue
    in1 = i.find(" golden globe for best")
    in2 = i.find(" nominated for best")
    if (in1 != -1):
      new.append(i[in1 + 18:])
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
  stop_signal = [".", "#", ",","?", "for", "!", ":", "goes to", "should", "at", "@", "like"]
  for i in range(len(awards)):
    lowest = 100
    for j in stop_signal:
      temp = awards[i].find(j)
      if (temp < lowest and temp != -1):
        lowest = temp
    new.append(awards[i][:lowest])
  return new

def is_in(word1, word2):
  split1 = word1.split()
  for i in split1:
    if (not (i in word2)):
      return False
  return True

def is_similar(word, word_list):
  out = word_list.copy()
  for i in range(len(word_list)):
    east = is_in(word_list[i], word)
    west = is_in(word, word_list[i])
    if (east):
      out[i] = word
      return out
    elif (west):
      return out
  out.append(word)
  return out  
    

def longest_discrete(awards):
  finalized = []
  for i in awards:
    finalized = is_similar(i, finalized)
  finalized = compress(finalized)
  finalized.sort(key=sizeify)
  return finalized[-26:]
      
def sizeify(word):
  return len(word)

def compress(a):
  seen = set()
  result = []
  for item in a:
    if item not in seen:
      seen.add(item)
      result.append(item)
  return result

def awards_get(tweets):
    awards = []
    relevant = get_contains(tweets," golden globe for best", "goldenglobes")
    awards.extend(relevant)
    relevant = get_contains(tweets," nominated for best", "goldenglobes")
    awards.extend(relevant)
    awards = clean_awards(awards)
    banned = ["something", "anything", "everything", "oscar", "golden globe", "academy award", "academyaward", "emmy", "awards"]
    remove_banned(awards, banned)
    awards = filter_noise(awards)
    final = longest_discrete(awards)
    return final


