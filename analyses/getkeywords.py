import pandas as pd

def get_prototypes(ll, num=10):
    #get the indice of 10 documents with highest probability for each label
    result = {}
    labels = list(ll.columns)
    for i in range(ll.shape[1]):
        tmp = pd.DataFrame(list(range(ll.shape[0])), columns=['index'])
        tmp['value'] = ll[labels[i]]
        tmp = tmp.sort_values(by = 'value', ascending = False)
        result[labels[i]] = list(tmp['index'].iloc[:num])
    return result

def get_keywords(features, prototypes, num=100):
    result = pd.DataFrame()
    words = list(features.columns)
    for label in prototypes.keys():
        tmp = pd.DataFrame()
        tmp['words'] = words
        tmp['tfidf'] = list(features.iloc[prototypes[label],:].sum(axis=0))
        tmp = tmp.sort_values(by = 'tfidf', ascending = False)
        result[label] = list(tmp['words'].iloc[:num])
    return result

def common_keywords(title1, title2, keywords):
    #get a list of words that are shared in the top 50 keywords in both titles
    return [word for word in list(keywords[title1]) if word in list(keywords[title2])]


def contributing_words(cleaned_words, keywords):
    """
    Write a function to get a list of words that appear in the
    top 100 keywords for each label.
    """
    result = {}
    for word in cleaned_words:
        for label in keywords.columns:
            if label not in result.keys():
                result[label] = []
            if word in list(keywords[label]):
                result[label].append(word)
    for label in result.keys():
        result[label] = (", ").join(result[label])
    return result
