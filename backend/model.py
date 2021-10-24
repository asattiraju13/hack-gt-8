#!/usr/bin/env python
# coding: utf-8
import re
import math
import numpy as np

from stop_words import get_stop_words
stop_words = set(get_stop_words('en'))

def tokenize(string):
    string = re.sub(r'[^\w\s]','',string.lower())
    return string.split(" ")

def idf(documents):
    count = {}
    for doc in documents:
        for word in set(tokenize(doc)):
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
    for c, k in count.items():
        count[c] = math.log(len(documents)/k)
    return count

def tf(document):
    document = tokenize(document)
    d = {}
    for word in document:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    for k, v in d.items():
        d[k] = v/len(document)
    return d

def tfidf(s1, s2, idf):
    t1 = tf(s1)
    t2 = tf(s2)
    out1 = []
    out2 = []
    words = set(tokenize(s1) + tokenize(s2))
    for word in words:
#         print(word)
        if word in t1:
            out1.append(t1[word] * idf[word])
        else:
            out1.append(0)
        if word in t2:
            out2.append(t2[word] *idf[word])
        else:
            out2.append(0)
    return out1, out2

def similarity(s1, s2, idf):
    s1, s2 = tfidf(s1, s2, idf)
    s1, s2 = np.array(s1), np.array(s2)
    return np.dot(s1, s2)/(np.linalg.norm(s1)*np.linalg.norm(s2))

import nltk

tokenizer = nltk.RegexpTokenizer(r"\w+")

def remove_stop(string):
    new = []
    for i in string.split(' '):
        if i not in stop_words:
            new.append(i)
    return ' '.join(new)

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
        self.idf = idf(self.processed_sentences)
        
    def update(self, new_string):
        raw_new_sentences = new_string.split(". ")
        new_sentences = []
        for i, v in enumerate(raw_new_sentences):
            new_sentences.append(' '.join(tokenizer.tokenize(remove_stop(v.lower()))))
        print(new_sentences)
        self.idf = idf(self.processed_sentences + new_sentences)
        similarities = [[0 for i in range(len(new_sentences))] for j in range(len(self.processed_sentences))]
        for i, v in enumerate(self.processed_sentences):
            for j, w in enumerate(new_sentences):
                similarities[i][j] = similarity(v, w, self.idf)
        s = [-1 for j in range(len(similarities[0]))]
        for i in range(len(similarities)):
            for j in range(len(similarities[0])):
                s[j] = max(s[j], similarities[i][j])
        for i in range(len(similarities)):
            for j in range(len(similarities)):
                print(self.processed_sentences[i])
                print(new_sentences[j])
                print(similarities[i][j])
                print()
        print(s)
        similar_pairs = []
        js = {}
        for i in range(len(similarities)):
            for j, s in enumerate(similarities[i]):
                if s >= CUTOFF:
                    similar_pairs.append((i, j))
                    if j not in js:
                        js[j] = (i, s)
                    else:
                        if s > js[j][1]:
                            js[j] = (i, s)
       
        """
        TODO: Make it add it at the proper point
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
                    posn = js[last[j]][0]
                if posn < len(final_raw):
                    final_raw.insert(posn+1, raw_new_sentences[j])
                    final_processed.insert(posn+1, new_sentences[j])
                else:
                    final_raw.append(raw_new_sentences[j])
                    final_processed.append(new_sentences[j])
        self.raw_sentences = final_raw
        self.processed_sentences = final_processed
