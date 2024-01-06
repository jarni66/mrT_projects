from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
from docx import Document
from htmldocx import HtmlToDocx
import requests
from docx.shared import Inches
import undetected_chromedriver as uc 
import re
import os
import shutil
from PIL import Image
from io import StringIO

# def to_doc(x):

#     if x.name == 'p':
#         document.add_paragraph(x.text)
#     elif x.name == 'ol':
#         li = x.find_all('li')
#         for j in li:
#             document.add_paragraph(j.text,style='List Bullet')






# with open('question/done_link.json') as f:
#     dones = json.load(f)

# dones = [int(i['link'].split('/')[-1]) for i in dones]

chrome_options = uc.ChromeOptions() 
chrome_options.headless = False  # Set headless to False to run in non-headless mode

driver = uc.Chrome(options=chrome_options)
link_done = []
link_fail = []
url_home = 'https://www.rumah.com/tanya-properti' 
driver.get(url=url_home)
soup = BeautifulSoup(driver.page_source, 'html.parser')

listing_card = soup.find_all('li',{'class':'askguru-category__item'})
card_links = [i.find('a').get('href') for i in listing_card]

data = []

scraped_item = 0
for card in card_links:
    card_name = card.split('1')[0]
    url = 'https://www.rumah.com' + card
    driver.get(url=url)
    soup_card = BeautifulSoup(driver.page_source, 'html.parser')
    paging = soup_card.find('ul',{'class':'pagination'})
    last_page = paging.find_all('li')
    last_page = [i.text for i in last_page]
    try:
        last_page = int(last_page[-3].replace('\n','').strip())
        for page in range(1,last_page+1):
            print(f"SCRAPE {card_name} : page {page} ### output lenght {len(data)}")
            url_page = 'https://www.rumah.com' + card_name + str(page)
            try:
                
                driver.get(url=url_page)
                soup_page = BeautifulSoup(driver.page_source, 'html.parser')
                items = soup_page.find('div',{'class':'list-of-questions'})
                item_list = items.find_all('article')
                for article in item_list:
                    try:
                        record = {}
                        name = article.find('span',{'class':'question-screen-name'}).text
                        category = article.find('a',{'class':'question-category'}).text
                        question_date = article.find('div',{'class':'question-poster-info__sub-info'}).text
                        question = article.find('div',{'class':'question-content'}).text
                        question_url = article.find('div',{'class':'question-content'}).find('a').get('href')
                        likes = article.find('span',{'class':'likes-count'}).text
                        view = article.find('span',{'class':'view-count'}).text
                        asnwer = article.find('span',{'class':'answer-count'}).text

                        record['name'] = name
                        record['category'] = category
                        record['question_date'] = question_date
                        record['question'] = question.replace('\n','').strip()
                        record['question_url'] = 'https://www.rumah.com' + question_url
                        record['likes'] = likes
                        record['view'] = view.replace('\n','').strip()
                        record['asnwer'] = asnwer.replace('\n','').strip()

                        data.append(record)
                        with open('question/output.json', 'w') as f:
                            json.dump(data, f)
                    except:
                        pass
                done = {'link': url_page}
                link_done.append(done)
                with open('question/done_link.json', 'w') as f:
                    json.dump(link_done, f)
            except:
                fail = {'link': url_page}
                link_fail.append(fail)
                with open('question/fail_link.json', 'w') as f:
                    json.dump(link_fail, f)
    except:
        pass
   