#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 22:25:50 2019

@author: mrinalmanu
"""

import nltk
import gensim
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# load text
text = open('/home/mrinalmanu/Documents/1mcorpus/corpus.en_ru.1m.ru', 'r', encoding='utf-8').read()

def tokenize_ru(file_text):
# firstly let's apply nltk tokenization
    tokens = word_tokenize(file_text)

# let's delete punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

# deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]

# cleaning words
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]

    return tokens

sentences = [tokenize_ru(sent) for sent in sent_tokenize(text, 'russian')]

# train model
model = gensim.models.Word2Vec(sentences, size=150, window=5, min_count=5, workers=4)

# save model
model.save('/home/mrinalmanu/Documents/1mcorpus/w2v.model')
print('saved')

#______________________________________________________________________________
# Let's attach some grammatical description to each word and repack sentences
# This is for Russian language!

new_tagged = []

def process_content():
    try:
        for i in sentences:
            new_tagged.append('\n')
            for element in i:
                words = tokenize_ru(element)
                tagged = nltk.pos_tag(words, lang='rus')   
                new_tagged.append(tagged)                   
    
    except Exception as e:
        print(str(e))
        
new_tagged.append(process_content())


# using list comprehension + zip() + slicing + enumerate() 
# Split list into lists by particular value 
def repack_sentences(test_list):
    
    size = len(test_list) 
    idx_list = [idx + 1 for idx, val in
            enumerate(test_list) if val == '\n'] 
  
  
    res = [test_list[i: j] for i, j in
        zip([0] + idx_list, idx_list + 
        ([size] if idx_list[-1] != size else []))] 

    return res



russian_corpus_final = repack_sentences(new_tagged)

#______________________________________________________________________________
# LET'S WORK ON ENGLISH CORPUS

text = open('/home/mrinalmanu/Documents/1mcorpus/corpus.en_ru.1m.en', 'r', encoding='utf-8').read()


def tokenize_en(file_text):
# firstly let's apply nltk tokenization
    tokens = word_tokenize(file_text)

# let's delete punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

# deleting stop_words
    stop_words = stopwords.words('english')
    tokens = [i for i in tokens if (i not in stop_words)]

    return tokens

sentences = [tokenize_en(sent) for sent in sent_tokenize(text, 'english')]

# train model
model_english = gensim.models.Word2Vec(sentences, size=150, window=5, min_count=5, workers=4)

# save model
model_english.save('/home/mrinalmanu/Documents/1mcorpus/w2v.model_english')
print('saved')

#______________________________________________________________________________
# Let's attach some grammatical description to each word and repack sentences
# This is for English language!

new_tagged_en = []

def process_content_en():
    try:
        for i in sentences:
            new_tagged_en.append('\n')
            for element in i:
                words = tokenize_en(element)
                tagged = nltk.pos_tag(words, lang='eng')   
                new_tagged_en.append(tagged)                   
    
    except Exception as e:
        print(str(e))
        
new_tagged_en.append(process_content_en())


# using list comprehension + zip() + slicing + enumerate() 
# Split list into lists by particular value 
def repack_sentences_en(test_list):
    
    size = len(test_list) 
    idx_list = [idx + 1 for idx, val in
            enumerate(test_list) if val == '\n'] 
  
  
    res = [test_list[i: j] for i, j in
        zip([0] + idx_list, idx_list + 
        ([size] if idx_list[-1] != size else []))] 

    return res


english_corpus_final = repack_sentences(new_tagged_en)

#______________________________________________________________________________



for elements in russian_corpus_final:
    
    
    