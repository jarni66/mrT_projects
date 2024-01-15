import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time
import os
import aiohttp
import asyncio

def get_page_listing(page):
    url_page = f'https://halorumah.id/search-results/page/{page}/?keyword&min-price&max-price&location%5B0%5D'

    response = requests.get(url_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings_url = soup.find_all('h2',{'class':'item-title'})
    listings_url = [i.find('a').attrs['href'] for i in listings_url]
    return listings_url

def get_agent_page_contact(url):
    def get_phone(elem):
        try:
            phone = elem.find('span',{'class':'agent-phone'}).text
        except:
            phone = None
        return phone

    def get_email(elem):
        try:
            email = elem.find('li',{'class':'email'}).find('a').text
        except:
            email = None
        return email
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')


        agents_phone = get_phone(soup)
        agents_email = get_email(soup) 


        return agents_phone,agents_email
        
    except:
        agents_phone = None
        agents_email = None
        return agents_phone,agents_email

def get_listing_details(url):
    
    def get_city(elem):
        try:
            city = elem.find('li',{'class':'detail-city'}).find('span').text
        except:
            city = None
        return city
    
    def get_prov(elem):
        try:
            prov = elem.find('li',{'class':'detail-state'}).find('span').text
        except:
            prov = None
        return prov
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('div',{'class':'page-title'}).text.replace('\n','')
        desc = soup.find('div',{'class':'block-content-wrap'}).text.replace('\n','')
        price_tag = soup.find('li',{'class':'item-price'}).text
        full_address = soup.find('ul',{'class':'list-1-cols list-unstyled'}).find_all('span')
        full_address = ' '.join([i.text for i in full_address])
        city = get_city(soup)
        province = get_prov(soup)
        prop_cat = soup.find('ol',{'class':'breadcrumb'}).find_all('li')[1].text
        prop_type = soup.find('div',{'class':'property-labels-wrap'}).text.split('\n')
        prop_type = [i.strip() for i in prop_type if i.strip() != '']

        agent_name = soup.find('li',{'class':'agent-name'}).text.strip()
        agent_url = soup.find('li',{'class':'agent-link'}).find('a').attrs['href']
        agent_email = get_agent_page_contact(agent_url)[1]
        agent_phone = get_agent_page_contact(agent_url)[0]
        agent_wa = get_agent_page_contact(agent_url)[0]
        images = soup.find_all('div',{'itemprop':'associatedMedia'})
        images = [i.find('img').attrs['data-lazy'] for i in images]

        data = {
            'url': url,
            'title': title,
            'desc': desc,
            'price': price_tag,
            'address': full_address,
            'city': city,
            'province': province,
            'propertyCategory': prop_cat,
            'propertyType': prop_type,
            'agent_name': agent_name,
            'agent_url': agent_url,
            'agent_email': agent_email,
            'agent_phone': agent_phone,
            'agent_wa': agent_wa,
            'images' : images
        }
        print(f"DONE {url}")
        return data
        
    except:
        print(f"FAIL {url}")
        data = None
        return data

def get_folder():
    file_names = os.listdir('listings_data2')
    datas = []
    for name in file_names:
        name = name.split('.')[0].split('_')[-1]
        datas.append(int(name))
    return datas



async def fetch_listings_url(page, session):
    
    url_page = f'https://halorumah.id/search-results/page/{page}/?keyword&min-price&max-price&location%5B0%5D'

    try:
        async with session.get(
            url_page, 
            # headers=headers,
            ssl = False, 
            # encoded = True,
            timeout = aiohttp.ClientTimeout(
                total=None, 
                sock_connect = 10, 
                sock_read = 10
            )
        ) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

            listings_url = soup.find_all('h2',{'class':'item-title'})
            listings_url = [i.find('a').attrs['href'] for i in listings_url]

         
        return listings_url
    except Exception as e:
        return []


async def run(page_list):
    tasks = []
    # conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession() as session:
        for url in page_list:
            task = asyncio.ensure_future(fetch_listings_url(url,session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
   
    return responses



  

