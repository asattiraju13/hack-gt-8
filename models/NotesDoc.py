#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
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
    # implement later 3dspin kekw 


# In[2]:


a = ["This is my sentence.", "It's kinda pog not gonna lie", "I love potatoes"]
b = ["I enjoy large potatoes.", "They make good fries"]
out = []
for j in a:
    for k in b:
        out.append(similarity(j, k))
out


# In[3]:


import nltk
sentence  = "Think and wonder, wonder and think.".lower()

tokenizer = nltk.RegexpTokenizer(r"\w+")
new_words = tokenizer.tokenize(sentence)

print(new_words)


# In[4]:


CUTOFF = 0.9


# In[14]:


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


# In[15]:


a = NotesDoc("""We are interested in manipulating freely moving cables, in real time, with a pair of robotic grippers, and with no added mechanical constraints. The main contribution of this paper is a perception and control framework that moves in that direction, and uses real-time tactile feedback to accomplish the task of following a dangling cable. The approach relies on a vision-based tactile sensor, GelSight, that estimates the pose of the cable in the grip, and the friction forces during cable sliding.""")


# In[16]:


a.update("""The successful implementation of the tactile perception and model-based controller in the cable following task, and its generalization to different cables and to different following velocities, demonstrates that it is possible to use simple models and controllers to manipulate deformable objects. The illustrative demonstration of picking and finding the end of a headphone cable for insertion provides a example of how the proposed framework can play a role in practical cable-related manipulation tasks""")


# In[22]:


'                  '.join(a.raw_sentences)


# In[ ]:




