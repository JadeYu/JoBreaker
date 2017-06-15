import pandas as pd

def get_one_entry(result, target):
    """
    Given the results for one job post,
    put them into one dictionary (corresponding to one entry if converted to data frame).
    """
    one_entry = {}
    one_entry['state'] = result['state']
    one_entry['city'] = result['city']
    one_entry['company'] = result['company']
    one_entry['sponsored'] = result['sponsored']
    one_entry['jobtitle_orig'] = result['jobtitle']
    one_entry['jobtitle'] = target
    one_entry['jobkey'] = result['jobkey']
    one_entry['snippet'] = client.jobs(jobkeys = [result['jobkey']])['results'][0]['snippet']
    
    return one_entry

def title_filter(title, target):
    """
    Return True if the words in target appear in the title (in any order), otherwise False.
    """ 
    wtl = title.lower().split(" ")
    wtg = target.lower().split(" ")
    for w in wtg:
        if w not in wtl:
            return False 
    return True

#test
#title_filter('senior product data manager', 'manager product')

def API2csv(client, all_cities, title_list, title_abbr, path = '../../data/', max_attempt = 5):
    """
    For each city-title combination, submit query,
    format data and save into a .csv file.
    """
    for i in range(len(title_list)):
        target = title_list[i]
        for city in all_cities:
            succeed = False
            attempts = 0
            while not succeed and attempts < max_attempt:
                try: 
                    params = {
                        'q' : target,
                        'l' : city,
                        'jt' : "fulltime",
                        'limit': "100",
                        #country is US by default
                        'fromage': "100",
                        'radius': "25",
                        'userip' : "1.2.3.4",
                        'format' : "json",
                        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
                    }

                    search_response = client.search(**params)

                    table = pd.DataFrame()
                    for j in range(len(search_response['results'])):
                        result = search_response['results'][j]
                        if title_filter(result['jobtitle'], target):
                            table = table.append(pd.Series(get_one_entry(result, target), name = str(j)))

                    filepath = path+title_abbr[i]+'_'+city.split(",")[0]+'.csv'
                    table.to_csv(filepath)
                    succeed = True
                except:
                    attempts += 1
                    print("Query for {} in {} failed".format(title_abbr[i], city.split(",")[0]))
