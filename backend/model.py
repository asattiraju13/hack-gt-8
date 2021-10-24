#!/usr/bin/env python
# coding: utf-8

import spacy
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_sm')

stop = stopwords.words("english")

def remove_stop(string):
    new = []
    for i in string.split(' '):
        if i not in stop:
            new.append(i)
    return ' '.join(new)

def similarity(s1, s2):
    s1 = nlp(remove_stop(s1))
    s2 = nlp(remove_stop(s2))
    return s1.similarity(s2)

tokenizer = nltk.RegexpTokenizer(r"\w+")
CUTOFF = 0.9

class NotesDoc:
    def __init__(self, string):
        sentences = string.split(". ")
        self.raw_sentences = sentences
        processed_sentences = []
        for i, v in enumerate(sentences):
            processed_sentences.append(' '.join(tokenizer.tokenize(remove_stop(v.lower()))))
#         print(sentences)
        self.processed_sentences = processed_sentences
        
    def update(self, new_string):
        raw_new_sentences = new_string.split(". ")
        new_sentences = []
        for i, v in enumerate(raw_new_sentences):
            new_sentences.append(' '.join(tokenizer.tokenize(remove_stop(v.lower()))))
        print(new_sentences)
        similarities = [[0 for i in range(len(new_sentences))] for j in range(len(self.processed_sentences))]
        for i, v in enumerate(self.processed_sentences):
            for j, w in enumerate(new_sentences):
                similarities[i][j] = similarity(v, w)
        print(similarities)
        similar_pairs = []
        js = {}
        for i in range(len(similarities)):
            for j, s in enumerate(similarities[i]):
                if s >= CUTOFF:
                    similar_pairs.append((i, j))
                    if j not in js:
                        js[j] = i
       
        """
        Make it add it at the proper point
        """
        last = [-1 for i in range(len(new_sentences))]
        for j in range(len(new_sentences)):
            if j in js:
                last[j] = j
            else:
                last[j] = -1 if j==0 else last[j-1]
        
        
        final_raw = self.raw_sentences
        final_processed = self.processed_sentences
        
        
        for j in range(len(new_sentences)):
            if j not in js:
                posn = 0
                if last[j] != -1:
                    posn = js[last[j]]
                final_raw.insert(posn, raw_new_sentences[j])
                final_processed.insert(posn, new_sentences[j])
        self.raw_sentences = final_raw
        self.processed_sentences = final_processed