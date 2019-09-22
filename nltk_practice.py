#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:10:25 2019

@author: mrinalmanu
"""
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# nltk.download()

#_________________________________________________________________________
# building a russian language corpus

ru_corp = open('/home/mrinalmanu/Documents/1mcorpus/corpus.en_ru.1m.ru')

corpus_of_russian = []

for item in ru_corp:
    corpus_of_russian.append(sent_tokenize(item))
    
corpus_of_russian_words = []
x = corpus_of_russian_words

for item in ru_corp:
    corpus_of_russian_words.append(word_tokenize(item))


#__________________________________________________________________________
# building an english language corpus    
    
en_corp = open('/home/mrinalmanu/Documents/1mcorpus/corpus.en_ru.1m.en')

corpus_of_english = []

for item in en_corp:
    corpus_of_english.append(sent_tokenize(item))
    
corpus_of_english_words = []

for item in en_corp:
    corpus_of_english_words.append(word_tokenize(item))

    
#__________________________________________________________________________
# Let's clean out stop words from our tokens
    
stop_words_english = list(stopwords.words('english'))
stop_words_russian = list(stopwords.words('russian'))    

ru_corp_filtered = []
en_corp_filtered = []

# converting lists of list in a flat list

flat_russian_corpus = [item for sublist in corpus_of_russian_words for item in sublist]
flat_english_corpus = [item for sublist in corpus_of_english_words for item in sublist]

ru_corp_filtered = [w for w in flat_russian_corpus if not w in stop_words_russian]
en_corp_filtered = [w for w in flat_english_corpus if not w in stop_words_english]

# While we will use corpus_of_russian_words for other analyses, for statistical
# purposes we are going to use a filtered corpus

# len(flat_english_corpus)
# Out[79]: 24189329

# len(en_corp_filtered)
# Out[80]: 15770719

# We can see that this significantly reduces the size of database

    
#__________________________________________________________________________
# We can also do stemming. Which means finding root word for the given word.

from nltk.stem import PorterStemmer

ps = PorterStemmer()

text = "some text here"

words = word_tokenize(txt)

for w in words:
    print(ps.stem(w))
  
