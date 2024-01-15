import requests
import re
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json
import pandas as pd
import os

class StoreItem:
    def __init__(self):
        self.items = []
    def add_item(self,item):
        self.items.append(item)
    def save_item(self,name):
        with open(name, 'w') as f:
            json.dump(self.items, f)
    def clear(self):
        self.items = []




def get_url_head(location,page):
    url = f"https://pergikuliner.com/restaurants?default_search={location}&page={page}"

    payload = {}
    headers = {
    'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'default_search=; _session_id=68248bdcda0191f3d9ef10002b3a5295; AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35AA25218FA77E626150EEFCBF2CCCF99AE487428771339881CEAD87D139427DCD0; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35AA25218FA77E626150EEFCBF2CCCF99AE487428771339881CEAD87D139427DCD0; _ga=GA1.2.546791218.1702718285; _gid=GA1.2.301794274.1702718285; _ga_QHWWGLQXQ8=GS1.2.1702718285.1.1.1702718335.10.0.0; _mkra_ctxt=7db949383d35f75868c39f2a2f12842f--200; _session_id=68248bdcda0191f3d9ef10002b3a5295',
    'Pragma': 'no-cache',
    'Referer': 'https://pergikuliner.com/restaurants',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-CSRF-Token': 'FeYdPJeQDb3l1KOfRi0Wx+TkI/sevGKvJuW8PGe1nJHDPvPzXOV6EptVptdU0kO60YRBqeIZaQ8ZXKO9su0uuQ==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    body = response.text

    pattern = re.compile(r'\$\("div#restaurant_contents"\)\.append\((.*?)\);')

    matches = pattern.findall(body)

    if matches:
        extracted_content = matches[0]
        # print(extracted_content)
    else:
        print("No match found.")

    html = extracted_content.replace('\\n','').replace('\\','')
    soup = BeautifulSoup(html,'html.parser')
    urls = soup.find_all('h3',{'class':'item-name'})
    urls = ['https://pergikuliner.com'+i.find('a').attrs['href'] for i in urls]

    return urls


def get_url_head2(location,page):
    url = f"https://pergikuliner.com/restoran/jakarta/{location}/?page={page}"

    payload = {}
    headers = {
    'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.546791218.1702718285; __gads=ID=59d4a7c491fa20cb:T=1702794062:RT=1702794964:S=ALNI_Mb-xDu1s92Ljcdr0j4pbNM7AdKZYw; _session_id=d6c1b32da132d6366a755220daf59cd2; _gid=GA1.2.324927161.1705225595; default_search=Jakarta; _ga_QHWWGLQXQ8=GS1.2.1705237693.7.1.1705239943.60.0.0; AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35AA25218FA77E626150EEFCBF2CCCF99AE63F1CD0E47B3058B0984A0D8E8982DDB; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35AA25218FA77E626150EEFCBF2CCCF99AE63F1CD0E47B3058B0984A0D8E8982DDB; _mkra_ctxt=3770681942fbf2acfb5917d6aa1bad1e--200; _session_id=d6c1b32da132d6366a755220daf59cd2; default_search=Jakarta',
    'Pragma': 'no-cache',
    'Referer': 'https://pergikuliner.com/restoran/jakarta/jakarta-timur/?page=2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-CSRF-Token': 'Q5iH5Z+sUd4zqAbOmCsf8hwXLafXmkTNa0XoHTMnu0arlW/Z4CJ3lhJYHNVxXzydSEqYrYmoX1KSk14Bhchk6w==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    body = response.text
    # print(type(body))
    pattern = re.compile(r'\$\("div#restaurant_contents"\)\.html\("(.*?)"\);')

    matches = pattern.findall(body)

    if matches:
        extracted_content = matches[0]
        # print(extracted_content)
        html = extracted_content.replace('\\n','').replace('\\','')
        soup = BeautifulSoup(html,'html.parser')
        urls = soup.find_all('h3',{'class':'item-name'})
        urls = ['https://pergikuliner.com'+i.find('a').attrs['href'] for i in urls]
    else:
        print("No match found.")
        urls = []


    return urls


def try_req(url):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_session_id=68248bdcda0191f3d9ef10002b3a5295; _ga=GA1.2.546791218.1702718285; _gid=GA1.2.301794274.1702718285; default_search=Jakarta; __gads=ID=59d4a7c491fa20cb:T=1702794062:RT=1702794964:S=ALNI_Mb-xDu1s92Ljcdr0j4pbNM7AdKZYw; AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35A647548A4AF06EF170F439B51681562957C251F864B709F1352FEA4DBEDC24AFC; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35A647548A4AF06EF170F439B51681562957C251F864B709F1352FEA4DBEDC24AFC; _ga_QHWWGLQXQ8=GS1.2.1702791315.2.1.1702796634.14.0.0; _mkra_ctxt=becdada535ef99c1fe6e69cc1b03c80f--200; _session_id=68248bdcda0191f3d9ef10002b3a5295; default_search=Jakarta',
    'Pragma': 'no-cache',
    'Referer': 'https://pergikuliner.com/restaurants?utf8=%E2%9C%93&search_place=&default_search=Jakarta&search_name_cuisine=&commit=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = parse(soup)
    
    return result

def parse(soup,url):
    resto = soup.find('div',{'class':'heading'}).text.replace('\\n','').strip()
    culinary = soup.find('span',{'itemprop':'servesCuisine'}).text
    street = soup.find('span',{'class':'left'}).text.replace('\\n','').strip()
    street = re.sub(r'\s+', ' ', street)
    locations = soup.find('div',{'class':'breadcrumbs'})
    area = locations.find_all('span',{'itemprop':'name'})[3].text.strip()
    district = locations.find_all('span',{'itemprop':'name'})[2].text.strip()
    city = locations.find_all('span',{'itemprop':'name'})[1].text.strip()
    phone = soup.find('p',{'class':'large-screen-toggle'}).find_all('a')
    phone = [i.text for i in phone]

    email = ''
    website = ''
    info = soup.find('div',{'class':'info-list'}).find_all('li')
    for i in info:
        if 'Website' in i.find('span').text:
            website = i.find(string=True,recursive=False)
        elif 'Email' in i.find('span').text:
            email = i.find(string=True,recursive=False)
    keyword = soup.find('div',{'class':'keyword-box'}).find_all('a')
    keyword = [i.text for i in keyword]

    result = {
        'resto': resto,
        'culunary':culinary,
        'street':street,
        'area':area,
        'district':district,
        'city':city,
        'phone':phone,
        'email':email,
        'website':website,
        'keyword':keyword,
        'url':url
    }
    return result

async def get_details(urls,data):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_session_id=68248bdcda0191f3d9ef10002b3a5295; _ga=GA1.2.546791218.1702718285; _gid=GA1.2.301794274.1702718285; default_search=Jakarta; __gads=ID=59d4a7c491fa20cb:T=1702794062:RT=1702794964:S=ALNI_Mb-xDu1s92Ljcdr0j4pbNM7AdKZYw; AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35A647548A4AF06EF170F439B51681562957C251F864B709F1352FEA4DBEDC24AFC; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E4179D14A96516FD4E0DC9BD6F0BA23F35A647548A4AF06EF170F439B51681562957C251F864B709F1352FEA4DBEDC24AFC; _ga_QHWWGLQXQ8=GS1.2.1702791315.2.1.1702796634.14.0.0; _mkra_ctxt=becdada535ef99c1fe6e69cc1b03c80f--200; _session_id=68248bdcda0191f3d9ef10002b3a5295; default_search=Jakarta',
    'Pragma': 'no-cache',
    'Referer': 'https://pergikuliner.com/restaurants?utf8=%E2%9C%93&search_place=&default_search=Jakarta&search_name_cuisine=&commit=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url,headers=headers) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    result = parse(soup,url)
                    data.add_item(result)
            except:
                print('ERROR')

async def fetch(url, session, data):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}
    try:
        async with session.get(
            url, headers=headers, 
            ssl = False, 
            timeout = aiohttp.ClientTimeout(
                total=None, 
                sock_connect = 20, 
                sock_read = 20
            )
        ) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            result = parse(soup,url)
            data.add_item(result)
    except Exception as e:
        print(e)
        # return (url, 'ERROR', str(e))

async def run(url_list,data):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch(url, session, data))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
    return responses

def test_main(reg,last_page):
    data = StoreItem()
    
    pages = range(1,3)
    for page in pages:
        urls = get_url_head(reg,page)
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(run(urls,data))
        loop.run_until_complete(task)
        result = task.result().result()

    print(data.items)

def get_district():
    df = pd.read_excel('pergikuliner_resto.xlsx')
    district = df['district'].unique().tolist()
    district = [i.lower().strip().replace(' ','-') for i in district]
    return district



def get_outlist():
    files = os.listdir('OUTPUT3')
    files = [i.replace('.json','') for i in files]
    return files

def get_output():
    regions = ['Jakarta', 'Bogor', 'Depok', 'Tangerang', 'Bekasi', 'Bandung', 'Surabaya']
    datas = []
    for reg in regions:
        with open(f'OUTPUT/{reg}.json') as f:
            out = json.load(f)
        datas += out

    print(len(datas))


    
# test = get_url_head2('jakarta-timur',126)
# print(test)
    

# print(get_outlist())