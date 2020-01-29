import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def retrieve_html(url):
    """
    Takes URL as argument and returns content of its response.

    adpated version of function found here: http://tinasdatablog.com/2018/03/29/prediction-of-oscar-nominees/
    """
    # remember to use browser header here, or cannot retrieve full data from the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers = headers)
    html = response.content
    # soup = BeautifulSoup(html,'lxml')
    return html

def get_data_from_oscar_page(html, category, award_name):

    """
    Gets and formats data from oscar website for years 16-18.

    adpated version of function found here: http://tinasdatablog.com/2018/03/29/prediction-of-oscar-nominees/
    """

    soup = BeautifulSoup(html,'lxml')
    result = []
    for item in soup.find_all('div', {'class':'result-subgroup subgroup-awardcategory-chron'}):
            try:
                award_title = item.find('div',{'class':'result-subgroup-title'}).find('a',{'class':'nominations-link'}).contents[0]
                if award_title == category:
                    sub_groups = item.find_all('div',{'class':'result-details awards-result-actingorsimilar'})
                    for sub in sub_groups:
                        test_list = []
                        #print(sub)
                        star = sub.find('span',{'class':'glyphicon glyphicon-star'})
                        if star != None:
                            win = True
                        else:
                            win = False
                        film_title = sub.find('div',{'class':'awards-result-film-title'}).find('a',{'class':'nominations-link'}).contents[0]
                        statement = sub.find('div',{'class':'awards-result-nominationstatement'}).find('a',{'class':'nominations-link'}).contents[0]
                        test_list.append(film_title)
                        test_list.append(win)
                        test_list.append(statement)
                        # result[film_title] = sub_result
                        result.append(test_list)
            except Exception:
                pass

    for num, nomination in enumerate(result):
        if num <= 4:
            nomination.append(2016)
        elif 5 <= num <= 9:
            nomination.append(2017)
        elif 10 <= num <= 14:
            nomination.append(2018)

    df = pd.DataFrame.from_records(result, columns=['Film', 'Winner', 'Name', 'Year'])
    df['Award'] = award_name
    return df
