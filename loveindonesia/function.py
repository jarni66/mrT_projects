import requests
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio
from lxml import etree 

def getCat():
    url = 'https://www.loveindonesia.com/directory/en/jakarta/restaurant'
    response = requests.get(url=url)

    soup = BeautifulSoup(response.text, 'html.parser')

    heads = soup.find_all('div',{'class':'col col_info'})
    cat_urls = []
    for head in heads:
        if head.find('h3').text.strip() != '':
            cat_urls.append(head.find('a').attrs['href'])
    return cat_urls

def getCatNav(cat_url):
    print("Getting urls...")
    response = requests.get(url=cat_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        last_page = soup.find('div',{'class':'pagination space'}).find_all('a')[-1].text.strip()
    except:
        last_page = soup.find('div',{'class':'pagination space'}).find('span').text.strip()

    heads_sec = soup.find('div',{'class':'panel row space table'})
    heads = heads_sec.find_all('div',{'class':'col'})
    resto_urls = []
    for i in heads:
        try:
            link = i.find('h2',{'class':'title'}).find('a').attrs['href']
            resto_urls.append(link)
        except:
            pass

    curr_page = 1
    while int(last_page) != curr_page:
        curr_page += 1
        cat_url_page = cat_url + '/' + str(curr_page)
        response = requests.get(url=cat_url_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        heads_sec = soup.find('div',{'class':'panel row space table'})
        heads_page = heads_sec.find_all('div',{'class':'col'})
        for i in heads_page:
            try:
                link = i.find('h2',{'class':'title'}).find('a').attrs['href']
                resto_urls.append(link)
            except:
                pass
    print("Having urls...")
    
    return resto_urls

def getRestoDetails(resto_url):
    response = requests.get(url=resto_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('div',{'class':'panel space table'})

    resto = section.find('h1',{'class':'title_big'}).text.replace('\\n','').strip()
    address = section.find('div',{'itemprop':'address'}).text.replace('\\n','').strip()
    try:
        phone = section.find('div',{'class':'info_desc'}).find('h2').text
    except:
        phone = None

    det = section.find('div',{'class':'col detail'}).find('div',{'class':'space'}).find_all('div',{'class':'info_desc'})
    category = [i.text for i in det[0].find_all('a')]
    cuisine = [i.text for i in det[1].find_all('a')]

    return {
        'resto': resto,
        'culinary':category,
        'address':address,
        'phone':phone,
        'keyword':cuisine,
        'url':resto_url
    }


async def fetch(url, session):
    
    try:
        async with session.get(
            url,  
            ssl = False, 
            timeout = aiohttp.ClientTimeout(
                total=None, 
                sock_connect = 20, 
                sock_read = 20
            )
        ) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            section = soup.find('div',{'class':'panel space table'})

            resto = section.find('h1',{'class':'title_big'}).text.replace('\\n','').strip()
            address = section.find('div',{'itemprop':'address'}).text.replace('\\n','').strip()
            try:
                phone = section.find('div',{'class':'info_desc'}).find('h2').text
            except:
                phone = None

            det = section.find('div',{'class':'col detail'}).find('div',{'class':'space'}).find_all('div',{'class':'info_desc'})
            category = [i.text for i in det[0].find_all('a')]
            cuisine = [i.text for i in det[1].find_all('a')]

            return {
                'resto': resto,
                'culinary':category,
                'address':address,
                'phone':phone,
                'keyword':cuisine,
                'url':url
            }
    except Exception as e:
        return {
                'resto': '',
                'culinary':'',
                'address':'',
                'phone':'',
                'keyword':'',
                'url':url
            }
        
async def run(url_list):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
    return responses

def scrape_urls(url_list):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    task = asyncio.ensure_future(run(url_list))
    loop.run_until_complete(task)
    result = task.result().result()
    
    return result


def getNonResto():
    url = 'https://www.loveindonesia.com/directory/en/jakarta#'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dom = etree.HTML(str(soup)) 

    div = soup.find('div',{'class':'col_content row'})
    heads = div.find_all('div',{'class':'col'})
    bar = heads[9].find_all('a')
    bar_urls = [i.attrs['href'] for i in bar]

    # street = dom.xpath('/html/body/div[7]/div[2]/div[2]/div/div[2]/div[1]/div[10]/div/div[1]/div/h2/a')
    street = dom.xpath('/html/body/div[7]/div[2]/div[2]/div/div[2]/div[1]/div[10]/div')
    street_string = etree.tostring(street[0])
    hotel = dom.xpath('/html/body/div[7]/div[2]/div[2]/div/div[2]/div[1]/div[12]/div')
    hotel_string = etree.tostring(hotel[0])
    spa = dom.xpath('/html/body/div[7]/div[2]/div[2]/div/div[2]/div[1]/div[14]/div')
    spa_string = etree.tostring(spa[0])


    soup_ = BeautifulSoup((street_string+hotel_string+spa_string),'html.parser')
    urls_a = soup_.find_all('a')
    urls = [i.attrs['href'] for i in urls_a]

    

    

    return urls