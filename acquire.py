from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import numpy as np
import re



###################################################################
##############       Primary CodeUp Function       ##############
#######     acquires dataframe with title, url, content     #######
###################################################################

def scrape_codeup():

    df = codeup_hyperlinks()
    df = clean_hyperlinks(df)
    webpage_list = scrape_codeup_webpages(df)
    df = pd.DataFrame(webpage_list)
        
    return df


  ########################################################
####### acquire urls, cleans df, and scrapes codeup #######
  ########################################################

#######       acquire urls       #######
def codeup_hyperlinks():
    ''' 
    This function will scrape hyperlinks from codeups main page and return a dataframe filled with
    hyperlinks and the titles of the page.
    It parses the response from codeup.com using beautiful soup, saving it into an article.
    It then will search for all the A files, tossing the entries into a list. 
    Next, it will run through the list of A files, searching for href entries.
    Those entries will be added to a dataframe with the title of the A file and whatever came after the href
    '''
    
    # hard-coded starting points for our function
    codeup_url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(codeup_url, headers=headers)
    
    # beautiful soup parsing for starting point
    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find('div', id='main-content')
    
    # a list of all the items which are found on the codeup_url
    # it will contain hyperlinks under the reference 'href' used later
    codeup_a_list = soup.find_all('a')
    
    # creating empty dataframe
    df = pd.DataFrame(columns = ['title', 'url'])
    # getting the length of the list created above
    number = len(codeup_a_list)

    for i in range(number):

        try: 
            if re.search(f'^/', codeup_a_list[i]['href']):
                url = 'https://codeup.com' + codeup_a_list[i]['href']
            else: 
                url = (codeup_a_list[i]['href'])
        except:
            url = 'none'
            title = codeup_a_list[i].text
            df.loc[i] = [title, url]
            pass
        else:
            title = codeup_a_list[i].text
            df.loc[i] = [title, url]

    return df


#######       cleans dataframe       #######
def clean_hyperlinks(df, arg=0):
    '''
    This function takes in a dataframe of potential hyperlinks with a column named 'url'.
    It will clean up any items in the dataframe which do not actually contain hyperlinks beginning with http:// or https://
    '''
    if arg:
        remove_url_list = arg
    
    else:
        remove_url_list = []
    
        try:
            for item in range(df.shape[0]):
                if re.search(f'^[^h]', df['url'].loc[item]):
                    remove_url_list.append(item)

        except:
            pass            
   
    df = df.drop(index = remove_url_list)
    df = df.reset_index()
    df = df.drop(columns = ['index'])
    
    return df


####### fills list of dictionaries with webpage content #######
def scrape_codeup_webpages(df):

    headers = {'User-Agent' : 'Codeup Data Science'}
    number = df.shape[0]
    webpage_list = []
    no_content_list = []
    for num in range(number):

        try: 
            url = df['url'][num]
            
            # using a header which may allow scraping
            response = get(url, headers = headers)
            # using no header
            #response = get(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            #main_content = soup.find('div', id='main-content')
            entry_content = soup.find('div', class_ ='entry-content')
            title = codeup_blog_df['title'][num]
            url   = codeup_blog_df['url'][num]
            
            webpage_content = entry_content.text.strip()
            
        except:
            no_content_list.append(num)
            pass
                
        else:
            dictionary = {}
            dictionary['name'] = f'webpage_content_dictionary_{num}'
            dictionary = {
                'title': title,
                'url' : url,
                'num' : webpage_content
            }
            webpage_list.append(dictionary)

    return webpage_list