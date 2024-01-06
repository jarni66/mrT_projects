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
import requests
import undetected_chromedriver as uc 
import re
import os

def scrape_item():
    data = {}
    try:
        title = soup_prop.find('h1',{'class':'title'}).text
    except:
        try:
            title = soup_prop.find('h1').text.replace('\n','').strip()
        except:
            title = None

    try:
        address = soup_prop.find('p',{'class':'full-address__text'}).text
    except:
        try:
            address = soup_prop.find('div',{'class':'property-detail'}).text.replace('\n','').strip()
        except:
            address = None

    try:
        desc = soup_prop.find('div',{'class':'description'}).text
    except:
        try:
            desc = soup_prop.find('div',{'class':'listing-details-text compacted'}).text.replace('\n','').strip()
        except:
            desc = None

    try:
        price = soup_prop.find('h2',{'class':'amount'}).text
    except:
        try:
            price = soup_prop.find('div',{'class':'property-value'}).text.replace('\n','').strip()
        except:
            price = None

    try:
        prop_type = soup_prop.find('div',{'class':'meta-table__item__value-text'}).text
    except:
        try:
            prop_type = soup_prop.find('td',{'class':'value-block'}).text.replace('\n','').strip()
        except:
            prop_type = None

    try:
        agent_name = soup_prop.find('a',{'class':'actionable-link agent-name truncate-line'}).text
    except:
        agent_name = None

    try:
        agency = soup_prop.find('div',{'class':'agency'}).text
    except:
        try:
            agency = soup_prop.find('div',{'class':'dev-name'}).text.replace('\n','').strip()
        except:
            agency = None


    try:
        agent_phone = soup_prop.find('a',{'class':'actionable-link btn-outline-secondary btn'}).get('href')
    except:
        agent_phone = None

    try:
        prop_cat = soup_prop.find('div',{'class':'label'}).text
    except:
        prop_cat = None

    data['property_url'] = prop
    data['title'] = title
    data['address'] = address
    data['desc'] = desc
    data['price'] = price
    data['prop_type'] = prop_type
    data['prop_cat']= prop_cat
    data['agent_name'] = agent_name
    data['agency'] = agency
    data['agent_phone'] = agent_number
    data['wa_url'] = whatsapp_url

    return data
    

chrome_options = uc.ChromeOptions() 
chrome_options.headless = False  # Set headless to False to run in non-headless mode
driver = uc.Chrome(options=chrome_options)

link_done = []
link_fail = []
datas = []

url_home = 'https://www.rumah.com/agen-properti/search?' 
driver.get(url=url_home)
soup = BeautifulSoup(driver.page_source, 'html.parser')

last_page = int(soup.find('ul',{'class':'pagination'}).find_all('li')[-2].text)

for page in range(1, last_page+1):
    page_url = 'https://www.rumah.com/agen-properti/search/' + str(last_page)
    driver.get(url=page_url)
    soup_page = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup_page.find_all('div',{'class':'agent-card'})
    for index_card in range(len(cards)):

        card = cards[index_card]
        card_url = card.find('div',{'class':'agent-info-name'}).find('a').get('href')
        card_url = 'https://www.rumah.com' + card_url 


        driver.get(url=card_url)
        soup_card = BeautifulSoup(driver.page_source, 'html.parser')

        agent_id = card_url.split('-')[-1]
        # agent_name = soup_card.find('h1',{'class':'agent-fullname'}).text
        # agency_name = soup_card.find('div',{'class':'agent-agency'}).text.replace('\n','').strip()
        try:
            aget_job_title = soup_card.find('div',{'class':'agent-job-title'}).text.replace('\n','').strip()
        except:
            aget_job_title = None

        agent_number = soup_card.find('span',{'class','agent-phone-number agent-phone-number-original visible-print'}).text
        whatsapp_url = soup_card.find('a',{'class','agent-whatsapp'}).get('href')

        agent_props = {'resident_sell':f'https://www.rumah.com/properti-dijual?agent_id={agent_id}&market=residential',
                       'resident_rent':f'https://www.rumah.com/properti-disewa?agent_id={agent_id}&market=residential',
                       'commercial_sell':f'https://www.rumah.com/properti-dijual?agent_id={agent_id}&market=commercial',
                       'commercial_rent':f'https://www.rumah.com/properti-disewa?agent_id={agent_id}&market=commercial'}
        # resident_sell = f'https://www.rumah.com/properti-dijual?agent_id={agent_id}&market=residential'
        # resident_rent = f'https://www.rumah.com/properti-disewa?agent_id={agent_id}&market=residential'
        # commercial_sell = f'https://www.rumah.com/properti-dijual?agent_id={agent_id}&market=commercial'
        # commercial_rent = f'https://www.rumah.com/properti-disewa?agent_id={agent_id}&market=commercial'

        # properties_links = [resident_sell, resident_rent,commercial_sell,commercial_rent]
        for properties_link in agent_props.keys():
            driver.get(url=agent_props[properties_link])
            soup_page = BeautifulSoup(driver.page_source, 'html.parser')

            links_prop = soup_page.find_all('a',{'class':'nav-link'})
            links_prop = [i.get('href') for i in links_prop]

            scrape = 0
            for prop in links_prop:
                scrape += 1
                print(f"AGENTS PAGE {page}, n_AGENT {index_card}, CAT {properties_link}, SCRAPE {scrape}")
                
                driver.get(url=prop)
                soup_prop = BeautifulSoup(driver.page_source, 'html.parser')

                data = scrape_item()
                
                datas.append(data)

                with open('agent/test.json', 'w') as f:
                    json.dump(datas, f)

