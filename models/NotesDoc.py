#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import math
import numpy as np
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


# In[2]:


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


# In[3]:


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


# In[4]:


def similarity(s1, s2, idf):
    s1, s2 = tfidf(s1, s2, idf)
    s1, s2 = np.array(s1), np.array(s2)
    return np.dot(s1, s2)/(np.linalg.norm(s1)*np.linalg.norm(s2))


# In[5]:


import nltk
from nltk.corpus import stopwords

sentence  = "Think and wonder, wonder and think.".lower()

tokenizer = nltk.RegexpTokenizer(r"\w+")
new_words = tokenizer.tokenize(sentence)

stop = stopwords.words("english")

def remove_stop(string):
    new = []
    for i in string.split(' '):
        if i not in stop:
            new.append(i)
    return ' '.join(new)


# In[6]:


CUTOFF = 0.9


# In[7]:


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
                        js[j] = i
       
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
                    posn = js[last[j]]
                final_raw.insert(posn, raw_new_sentences[j])
                final_processed.insert(posn, new_sentences[j])
        self.raw_sentences = final_raw
        self.processed_sentences = final_processed
        


# In[8]:


a = NotesDoc("""Designing an Immobilized Metal ion Affinity (IMA) chromatographic process on large scale demands a thorough understanding to be developed regarding the adsorption behaviour of proteins on metal loaded IMA (IMAM(II)) gels and the characteristic adsorption parameters to be evaluated. This research investigation illustrates the significance of these aspects for the proposed fractionation of chicken egg-white proteins on these gels. Consequently, a systematic investigation of the adsorption characteristics of three chicken egg-white proteins viz., ovalbumin, conalbumin and lysozyme on Cu(II) and Ni(II) loaded IMA gels, iminodiacetate (IDA) and tris(2-aminoethyl)amine (TREN), has been undertaken. These gels differ in their selectivity towards the proteins of interest under the identical sets of experimental conditions. While TREN-Ni(II) was selective only for lysozyme, IDA-Cu(II), IDA-Ni(II) and TREN-Cu(II) showed varying affinities for all the three proteins. The equilibrium and kinetic data were analysed using various theoretical models and adsorption parameters were quantified. On the basis of these investigations, various strategies have been proposed for the efficient large-scale fractionation of chicken egg-white proteins on these gels.""")


# In[9]:


a.update("""The present research effort focussed on a thorough analysis of the adsorption behaviour of three eggwhite proteins namely, ovalbumin, conalbumin and lysozyme on four IMA-M(II) gels viz., IDA-Cu(II), TREN-Cu(II), IDA-Ni(II) and TREN:Ni(II), with the intent to develop an improved understanding of these interactions for designing large scale IMA separations. The equilibrium adsorption data was analyzed using Langmuir and Langmuir-Freundlich models and the characteristic adsorption parameters were evaluated. The kinetic data was analysed using kinetic rate constant model. On the basis of these comparative adsorption studies two strategies were proposed for designing efficient fractionation of egg-white proteins using IMAC at large scale. The first approach was based on the differential affinities of three egg-white proteins for a particular IMA gel and the second approach highlighted the significance of CASMAC scheme. Despite being specific for egg-white proteins, this study has important general implications on the design of any large-scale IMA separation process. The study illustrated that the characteristic adsorption parameters required for designing an IMA based chromatographic separation process on preparative scale can be estimated on the basis of systematically conducted small scale batch experiments. Also, the information derived from this study can be utilized for the process development using hybrid bioseparation techniques such as metal chelate displacement chromatography and
immobilized metal ion-membrane filtration. The efficacy of these parameters in predicting the performance of an actual separation process is currently under investigation.""")


# In[ ]:




