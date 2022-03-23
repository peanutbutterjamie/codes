#!pip install Selenium
import requests
import os
import re
import json
import pandas as pd
import time

#!pip install beautifulsoup4
#!pip install tqdm
#!pip install fake_headers

import urllib.parse
from urllib.parse import urlencode
from time import time as timer
from bs4 import BeautifulSoup
from fake_headers import Headers
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#!pip install tqdm
import time
from tqdm import tqdm
from tqdm import tqdm_notebook, tnrange
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pickle

import requests
from requests.exceptions import SSLError

import urllib
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


selected_urls = set()

def scrape_articles3(page, url):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9050)
    profile.accept_untrusted_certs = True
    path = "/usr/local/Cellar/geckodriver"
    driver = webdriver.Firefox(executable_path=path)
    try:
        driver.get(url+str(page))
        news_titles = driver.find_elements_by_css_selector(".news_tit")
        media=driver.find_elements_by_css_selector(".media_end_head_top_logo_img.light_type")
        news_list=[]
        for item in news_titles:
            temp_list={}
            temp_url=item.get_attribute('href')
            if temp_url in selected_urls: continue
            temp_list['URL']=item.get_attribute('href')
            resp=requests.get(temp_list['URL'])
            soup=BeautifulSoup(resp.text,'html.parser')
            try: 
                temp_list['Media']=soup.select_one('div.media_end_head_top>a>img')['title']
                temp_list['Date']=soup.select_one("div.media_end_head_info_datestamp_bunch>span")['data-date-time']
                temp_list['Title']=item.text
                temp_list['Text']=soup.find("div",{"id":"newsct_article"}).text
                news_list.append(temp_list)
            except: pass 
        selected_urls.add(temp_url)
        time.sleep(1)
        driver.quit()
        df=pd.DataFrame(news_list)
        return df
    except SSLError: pass
    except HTTPError: pass 
    except : pass

def generating_article_df3(keywords, start_date, end_date):
    page=1
    #page=list(range(1,4000,15)
    df_first=True
    while True:
        url="https://m.search.naver.com/search.naver?where=m_news&query={0}&sort=0&photo=0&field=0&pd=3&ds={1}&de={2}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&start=".format(keyword, start_date, end_date)
        try:
            df_new=scrape_articles3(page,url)  
            if df_first:
                df_first, df_final=False, df_new
            else:
                df_final=pd.concat([df_final, df_new],ignore_index=True)
                df_final.to_pickle('./crawling_df_'+start_date+"_"+end_date".pkl")
            page+=15
        except URLError:
            break
        except: break     
    return None

kwds = ["코로나", "코비드", "corona", "covid", "SARS-CoV-2", "우한"]
kwds = ["코로나", "코비드"]
generating_article_df3  (kwds,"2021.12.30","2021.12.31")