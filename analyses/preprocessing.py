import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import nltk
#nltk.download()
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

def status_to_words(raw_status,noun=False, titleoff = False):
    # Function to convert a raw status to a string of words
    # The input is a single string (a raw status update), and 
    # the output is a single string (a preprocessed status update)
    #
    # 1. Remove HTML
    status_text = BeautifulSoup(raw_status, "html.parser").get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", status_text)
    # remove http URLs
    letters_only = re.sub(r"[^https?:\/\/.*[\r\n]*]", "", letters_only)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. Lemmatize word (e.g. to merge noun and pronoun)
    #stemmer = PorterStemmer()
    #stemmer = SnowballStemmer("english")
    wnl = WordNetLemmatizer()
    words = [wnl.lemmatize(word) for word in words]
    
    # In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #Remove a few more trivial words not identified by NLTK
    stops = stops.union([u'hasn',u'm',u've',u'll',u're',u'didn',u'us',
                         u'im',u'doesn',u'couldn',u'won',u'isn',u'http',
                           u'www',u'like',u'one',u'would',u'get',u'want',
                         u'really',u'could',u'even',u'much',u'make',u'good']) 
    if titleoff:
        stops = stops.union([u'data',u'analyst',u'analysis',u'analytics',u'science',u'scientist',
                         u'engineer',u'engineering',u'architect',u'architecture',u'product',
                         u'manage',u'management',u'manager',u'business',u'database',u'administration',
                        u'administrator',u'dba'])
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

def raw_cleaning(texts, noun, titleoff=False):
    raw_texts = list(texts)
    cleaned = []
    for i in range(len(raw_texts)):
        cleaned.append(status_to_words(raw_texts[i],noun, titleoff))
    return pd.Series(cleaned)

def get_grams(texts, noun):
    raw_texts = list(texts)
    cleaned = []
    for i in range(len(raw_texts)):
        cleaned.append(status_to_words(raw_texts[i],noun))
    
    vectorizer = CountVectorizer(analyzer = "word",   
                                     tokenizer = None,    
                                     preprocessor = None, 
                                     stop_words = None,   
                                     max_features = 10000,
                                     ngram_range = (1,2))
    vectorizer.fit_transform(cleaned)
    return vectorizer.get_feature_names()


def kfold_split(data, k):
    test_size = int(data.shape[0]/k)
    train_size = data.shape[0] - test_size
    data_train, data_test = train_test_split(data, train_size=train_size)
    return data_train, data_test
