from functools import reduce
from nltk import *
import string
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas 

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
    and returns a dictionary with the probability. Only catches
    words with more than 1% probability
    """
    total_words = len(dict_alice)
    all_dict = {word:(freq*100/total_words) for (word,freq) in dict.items()}
    return {word:freq for (word, freq) in all_dict.items() if freq > 1}

def get_hist(dict):
    #getting the frecuency of each word in # (if the word has a 100% of probability to appear in the text, it has 50 #)
    return (dict[0], math.ceil(dict[1] / 2) * '🐇')
       
def display_histogram(prob_dict):
    #print each word with its number of # in a different line (display the histogram)
    histogram = dict(map(get_hist, prob_dict.items()))  
    for key, value in histogram.items():
        print(key,':', value)

# Now we clean the data with the functions we created 
text_normAlice = normalize(raw_alice)
stop_alice = remove_stopwords(text_normAlice)
dict_alice = word_count(stop_alice)
prob_alice = word_probability(dict_alice)

"""
Now that our data is clean we can choose how do we want to visualize it
"""

# First of all we'll save it in a csv to access the info when we need it again
column_names = ["Word", "Prob"]
data_frame = []
for key, value in prob_alice.items():
    data_frame.append({"Word": key, "Count": value})
df = pandas.DataFrame(data_frame)
df.to_csv("Alice.csv")


while True:
    # We ask the user what they want to do
    print("Hello! How do you want to visualize this data?")
    print("1. A histogram with emojis! 🐇 \n2. A picture histogram 📈 ")
    answer = input(" ")
    if answer == "1":
        print(display_histogram(prob_alice))
        break
    elif answer == "2":
        df = df.sort_values("Count", ascending = False)
        pal = sns.color_palette("RdPu", len(df))
        pal.reverse()
        result = sns.barplot(data=df, x='Word', y='Count', palette=pal)
        result.set_title("Word Frequency")
        result.set_ylabel("Frequency")
        plt.xticks(rotation = 90)
        plt.show()
        break
    else: 
        print('I don\'t understand, please try again')
        continue

