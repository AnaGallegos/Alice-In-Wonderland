from functools import reduce
from nltk import *
import string
import math
import matplotlib.pyplot as plt
import seaborn as sns

"""First, we get our text and we turn it into a string"""
alice = open("Alice.txt", "r", encoding="utf8")
raw_alice = alice.read()
alice.close()
raw_alice = raw_alice.replace("—", " ").split()


"""We create a set with all the stopwords"""
english_read = open("stopwords_english.txt", "r", encoding="utf-8-sig")
stop_words = english_read.read()
english_read.close()
stop_words = set(stop_words.replace("'", "’").split())



def remove_stopwords(text):
    # Recives a list and creates a new list with no stop words
    return [w for w in text if w.lower() not in stop_words and len(w) > 0]

def remove_suff(text):
    # recives a word and removes the suffixes from the string
    alphabet = string.ascii_lowercase
    clean = ""
    for symbol in text.lower():
        if symbol in alphabet:
            clean += symbol
        elif symbol == "’":
            break
        else: continue
    return clean

def no_punctuation(word):
    punc = string.punctuation
    as_list =  list(filter(lambda x : x not in punc, word))
    return reduce(lambda x, y : x + y, as_list, "")


def normalize(text):
    #Removes stopwords
    text_lower = [w.lower() for w in text]
    # Removes suffixes
    clean2 = [remove_suff(x) for x in text_lower]
    # And removes punctuations
    return [no_punctuation(x) for x in clean2]

def word_count(text):
    """
    Recives a list of words and creates 
    the frequency of each word in a dictionary"""
    dict = {}
    for word in text:
        if word not in dict:
            dict[word] = 1
        else:
            dict[word] += 1
    return dict
    
def word_probability(dict):
    """
    Recives a dictionary with the frequency of each word
    and returns a dictionary with the probability
    """
    total_words = len(dict_alice)
    all_dict = {word:(freq*100/total_words) for (word,freq) in dict.items()}
    return {word:freq for (word, freq) in all_dict.items() if freq > 1}

def get_hist(dict):
    #getting the frecuency of each word in # (if the word has a 100% of probability to appear in the text, it has 50 #)
    return (dict[0], math.ceil(dict[1] / 2) * '#')
       
def display_histogram(prob_dict):
    #print each word with its number of # in a different line (display the histogram)
    histogram = dict(map(get_hist, prob_dict.items()))  
    for k, v in histogram.items():
        print(k,':', v)

text_normAlice = normalize(raw_alice)
stop_alice = remove_stopwords(text_normAlice)
dict_alice = word_count(stop_alice)
prob_alice = word_probability(dict_alice)
print(display_histogram(prob_alice))

hist = sns.barplot(data= prob_alice, x=prob_alice.items(), y="count")
hist.set_title("Histogram of Word Frequency", fontsize=40)
hist.set_ylabel("frequency",fontsize=25)
plt.xticks(rotation=45, fontsize=15)
plt.show()
