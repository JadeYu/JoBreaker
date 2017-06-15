import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords # Import the stop word list

def status_to_words(raw_status,noun=False):
    # Function to convert a raw status to a string of words
    # The input is a single string (a raw status update), and 
    # the output is a single string (a preprocessed status update)
    #
    # 1. Remove HTML
    status_text = BeautifulSoup(raw_status).get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", status_text)
    # remove http URLs
    letters_only = re.sub(r"[^https?:\/\/.*[\r\n]*]", "", letters_only)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #Remove a few more trivial words not identified by NLTK
    stops = stops.union([u'hasn',u'm',u've',u'll',u're',u'didn',u'us',
                         u'im',u'doesn',u'couldn',u'won',u'isn',u'http',
                           u'www',u'like',u'one',u'would',u'get',u'want',
                         u'really',u'could',u'even',u'much',u'make',u'good']) 
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    result = " ".join(meaningful_words)
    
    # 6. if noun option is true, extract only nouns
    if noun:
        tokens = nltk.word_tokenize(result)
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged\
                 if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        result = " ".join(nouns)
    
    return(result)

def raw_cleaning(texts):
    raw_texts = list(texts)
    cleaned = []
    for i in range(len(raw_texts)):
        cleaned.append(status_to_words(raw_texts[i],False))
    return pd.Series(cleaned)
