
# coding: utf-8

# In[72]:


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver




class Parser_wiki_ru(object):
    def __init__(self):
        chromedriver = '/usr/bin/chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # для открытия headless-браузера
        self.browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    def __reinit__(self):
        self.__init__()
    
    def get_runways(self, airport_name):    
        trys = 0
        sub_page = ""
        while trys<10:
            print(trys)
            self.browser.get('https://yandex.ru/')
            self.browser.find_element_by_id('text').send_keys(airport_name)
            self.browser.find_element_by_class_name("search2__button").click()
            page_search = self.browser.page_source
            find = page_search.find('''"https://ru.wikipedia.org/wiki/''')
            if find != -1:
                sub_page = page_search[find:]
                break
            trys+=1
        if sub_page == "":
            print(f"{airport_name} not found")
            return ""
            
        
        site_wiki = sub_page[:sub_page.find(''' data-counter=''')]
        site_wiki = site_wiki.split('''"''')[1]
        self.browser.get(site_wiki)
        air = self.browser.page_source
        soup = BeautifulSoup(air, 'html5lib')
        table = soup.find('table', attrs = {'class': ['infobox'], 'style': '', 'data-name': 'Аэропорт'})
        return table
    
    def parse_html_table(self, table):
        tags = []
        for row in table.find_all('tr'):
            #tag = row.find_all("span", class_ = "no-wikidata")
            tag = row.find_all("td", class_ = "plainlist")
            if len(tag)!=0:
                tr_tag = tag[0].find_all("tr")
                if len(tr_tag) != 0:
                    tr_tag = tr_tag[1:]
                    for tr in tr_tag:
                        num = "".join(re.findall(r'\d', tr.find_all("td")[1].text))
                        if len(num) >=4:
                            tags.append(int(num[:4]))
    
        hy = 0
        for row in table.find_all('tr'):
            tag = row.find_all("span", class_ = "no-wikidata")
            if len(tag)!= 0:
                if tag[0].attrs['data-wikidata-property-id'] == "P2044": 
                    hy  = int(re.findall(r'[-+]?\d+', tag[0].text)[0])
        return tags, hy
    
