import requests
import json
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import re
from requests_html import HTMLSession, AsyncHTMLSession
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import psycopg2
from lxml import etree 

class StoreItem:
    def __init__(self):
        self.items = []
        self.fails = []
    def add_item(self,item):
        self.items.append(item)
    def add_fail(self,fail):
        self.fails.append(fail)

    def save_item(self,name):
        with open(name, 'w') as f:
            json.dump(self.items, f)
        with open('fail_'+name, 'w') as f:
            json.dump(self.fails, f)
    def clear(self):
        self.items = []

def get_locationId(url):
    # url = "https://www.tripadvisor.co.id/Restaurants-g294225-Indonesia.html"
    
    headers = {
    'authority': 'www.tripadvisor.co.id',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'cache-control': 'no-cache',
    # 'cookie': 'TADCID=DjYuiIdohZyMuf31ABQCCKy0j55CTpGVsECjuwJMq3pRfrpkFFKmuz5NsP1nq7wganMbfEAkFnRGamormVL7I3fvwFusPFeaCFA; TASameSite=1; TAUnique=%1%enc%3AFuduJJsBkMKbwQcZTXQYEbq7XbAHKAY%2FBKypjtO5eK%2Ba9N54cyyFT5JpO2aDYKx8Nox8JbUSTxk%3D; TASSK=enc%3AAJojlGmkbrVRAVgohBTsA4Qm8NcLV49xwqgC45vcYeYxGlpsDGbDSnBvY4UrLUx1KUocjf%2FRrlgBK7mWOSzxg3lHwthpvzMA%2FKzpgjXoYgklVPc3ks78D5f1tr%2FEj613bQ%3D%3D; TART=%1%enc%3AaRoBz%2F%2BZBUxOpx7g77oKOdMI5v0JQ%2FHvbQW0kjul4z5w4gRQ9Jad87AYGr%2FhOj62rt3bdmzG49c%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1*RY.2023*RM.12*RD.20*RH.20*RG.2; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; pbjs_sharedId=922875ad-ef39-4602-b1a3-65cae8f083c1; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; _lc2_fpi=e3d9117eacb0--01hj112br4a8secqbx2nsfdw8q; _lc2_fpi_meta=%7B%22w%22%3A1702989213444%7D; _ga=GA1.1.1955129227.1702989214; _lr_sampling_rate=100; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID%22%3A%220ee2a1ae-b246-4f45-8c52-85529046e1bb%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-19T12%3A33%3A40%22%7D; pbjs_unifiedID_cst=zix7LPQsHA%3D%3D; pbjs_li_nonid=%7B%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; ServerPool=A; _li_dcdm_c=.tripadvisor.co.id; __gpi=UID=00000cb75f456717:T=1703009968:RT=1703009968:S=ALNI_MZTvSqOmmR5EeJVh5sKThNbGP-iAQ; PAC=AGN2UZtL3YT08NG5AiV-gph-ZFYSSyp3wOmve0ql3zJhRI95e5mXKDwhBuCfHy9QbmUX13wbLA2AEJGEwlfo3UYEk4_h482RzcVfu6ZtXTdqv9tXCledbc5O_NgrYHeC_Ht98tCUFElK1037k3f5lPgj1HRTp6Y8Y4pJUmu0ZWDq; PMC=V2*MS.6*MD.20231219*LD.20231220; TASID=001FF1C2FC7A42A4870290486A6AA22A; _lr_retry_request=true; __vt=UW5xTpAphCuVkL5MABQCCQPEFUluRFmojcP0P3EgGiozjw8oCcG_wby5YyQQyRBg3a1tYlTwDCQMY62AJ-KYdBk-6ZGjfjW85RWx38JWNHAa-1B5PtX43ow09zURbUC2M428cusg3vRfh4L1fiTyzEtQGw; ab.storage.deviceId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22fa636772-6f10-8a80-2391-096d6340da5f%22%2C%22c%22%3A1702989213823%2C%22l%22%3A1703057491244%7D; __gads=ID=5ec7cbf724913a72:T=1702989214:RT=1703057492:S=ALNI_MbYUYynUsTEPy-ctZrIc5nx5CApeg; TAReturnTo=%1%%2FRestaurants-g294225-oa40-Indonesia.html; roybatty=TNI1625!AEOljKyheDlqI4Xv8ZTehnXKm619be142XU7pkZ7PuEguEubVoMrcaBS1chJN1uYfOMjNkR4bV0tor74ZmT6zX0pvepoPfD%2Fw57jP6SWAZqeo475ZFf2eizJVy8kNfUuhFnNqIyWJUE047nFFMTotKo9mlp7LzD9LiyGvqgjjeQO4xYbJ5rvCLQK6N4y1kbPVg%3D%3D%2C1; TAUD=LA-1702989211239-1*RDD-1-2023_12_20*RD-20819352-2023_12_20.12314850*LG-68363774-2.1.F.*LD-68363775-.....; datadome=nsb8eKLxyuiBf8sDDTFTi0PzZZDKGnz8jd6YIW3R_FoEhUYy7KtS366lkQ8wp3zJTZuDZUpq7MXVV7BecQ1SVcrqIJDV7cib1O8bIoxCc7Z0pK5U7MyxO65YH2XXbf4Z; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Dec+20+2023+14%3A32%3A56+GMT%2B0700+(Western+Indonesia+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=acc56f53-bdd9-4e2b-828d-f6c950106d00&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _ga_QX0Q50ZC9P=GS1.1.1703055680.4.1.1703057578.60.0.0; ab.storage.sessionId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22fff6b864-2c61-dec2-ae48-e0fb9793e7d6%22%2C%22e%22%3A1703057638127%2C%22c%22%3A1703057491242%2C%22l%22%3A1703057578127%7D; TASession=V2ID.001FF1C2FC7A42A4870290486A6AA22A*SQ.35*LS.Restaurants*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.in*FA.1*DF.0*TRA.true*LD.297709*EAU._; EVT=gac.Restaurants_Controls*gaa.pagination*gal.pg_2*gav.0*gani.false*gass.Restaurants*gasl.294225*gads.Restaurants*gadl.294225*gapu.1f04663f-acbb-4f1f-b6c7-1a8cdcf3f9c8*gams.0; NPID=0',
    'pragma': 'no-cache',
    'referer': 'https://www.tripadvisor.co.id/Restaurants-g294225-Indonesia.html',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.110", "Google Chrome";v="120.0.6099.110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    session = HTMLSession()
    r =  session.get(url=url,
                     headers=headers, 
                     timeout=90)
    r.html.render(wait=3,
                  sleep=1,
                  reload=True)
    # print(r.html.html)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    with open("yourhtmlfile.html", "w", encoding='utf-8') as file:
        file.write(r.html.html)
    session.close()
    try:
        div = soup.find('div',{'class':'geos_grid'})
        loc_urls = div.find_all('a')
        urls = [i.attrs['href'] for i in loc_urls]
    except:
        div = soup.find('ul',{'class':'geoList'})
        loc_urls = div.find_all('a')
        urls = [i.attrs['href'] for i in loc_urls]
    return urls



def get_resto_urls(sec,location_link):
    url = "https://www.tripadvisor.co.id/data/graphql/ids"
    page = sec*30
    geo = location_link.split('-')[1][1:]
    paging = f"oa{page}"
    routepage = re.sub(r'(Restaurants-g\d+-)', r'\1' + paging + r'-', location_link)
    payload = json.dumps([
    {
        "variables": {
        "page": "Restaurants",
        "pos": "id-ID",
        "parameters": [
            {
            "key": "geoId",
            "value": geo
            },
            {
            "key": "offset",
            "value": f"{page}"
            }
        ],
        "factors": [
            "TITLE",
            "META_DESCRIPTION",
            "MASTHEAD_H1",
            "MAIN_H1",
            "IS_INDEXABLE",
            "RELCANONICAL"
        ],
        "route": {
            "page": "Restaurants",
            "params": {
            "geoId": int(geo),
            "offset": f"{page}"
            }
        }
        },
        "extensions": {
        "preRegisteredQueryId": "8ff5481f70241137"
        }
    },
    {
        "variables": {
        "routes": [
            {
            "page": "Restaurants",
            "params": {
                "geoId": int(geo),
                "offset": "0"
            }
            },
        ]
        },
        "extensions": {
        "preRegisteredQueryId": "6017922c6af2b8ff"
        }
    },
    {
        "variables": {
        "pageName": "Restaurants",
        "relativeUrl": routepage,
        "parameters": [
            {
            "key": "geoId",
            "value": geo
            },
            {
            "key": "offset",
            "value": f"{page}"
            }
        ],
        "route": {
            "page": "Restaurants",
            "params": {
            "geoId": int(geo),
            "offset": f"{page}"
            }
        }
        },
        "extensions": {
        "preRegisteredQueryId": "1a7ccb2489381df5"
        }
    },
    {
        "variables": {
        "page": "Restaurants",
        "params": [
            {
            "key": "geoId",
            "value": geo
            },
            {
            "key": "offset",
            "value": f"{page}"
            }
        ],
        "route": {
            "page": "Restaurants",
            "params": {
            "geoId": int(geo),
            "offset": f"{page}"
            }
        }
        },
        "extensions": {
        "preRegisteredQueryId": "f742095592a84542"
        }
    },
    {
        "variables": {
        "limit": 30,
        "racRequest": None,
        "route": {
            "page": "Restaurants",
            "params": {
            "geoId": int(geo),
            "offset": f"{page}"
            }
        },
        "additionalSelections": [
            {
            "facet": "ESTABLISHMENT_TYPES",
            "selections": [
                "10591"
            ]
            }
        ]
        },
        "extensions": {
        "preRegisteredQueryId": "18770219997e039d"
        }
    },
    {
        "variables": {
        "page": "Restaurants",
        "locale": "id-ID",
        "platform": "tablet",
        "id": geo,
        "urlRoute": routepage
        },
        "extensions": {
        "preRegisteredQueryId": "d194875f0fc023a6"
        }
    }
    ])

    headers = {
    'authority': 'www.tripadvisor.co.id',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'TADCID=DjYuiIdohZyMuf31ABQCCKy0j55CTpGVsECjuwJMq3pRfrpkFFKmuz5NsP1nq7wganMbfEAkFnRGamormVL7I3fvwFusPFeaCFA; TASameSite=1; TAUnique=%1%enc%3AFuduJJsBkMKbwQcZTXQYEbq7XbAHKAY%2FBKypjtO5eK%2Ba9N54cyyFT5JpO2aDYKx8Nox8JbUSTxk%3D; __vt=6TK59Vc5FaU4PGjzABQCCQPEFUluRFmojcP0P3EgGiovHsxbdN4gvpRavx3HJggax51UTViwHkb5Eo9dndEyKr4vTKBJwAB-SX7XvMw5jQZxyAWmfkKZBcqpy1TwXVeI3W0FfrYwbd7vP9erG0YVeQXn9A; TASSK=enc%3AAJojlGmkbrVRAVgohBTsA4Qm8NcLV49xwqgC45vcYeYxGlpsDGbDSnBvY4UrLUx1KUocjf%2FRrlgBK7mWOSzxg3lHwthpvzMA%2FKzpgjXoYgklVPc3ks78D5f1tr%2FEj613bQ%3D%3D; ServerPool=A; PMC=V2*MS.6*MD.20231219*LD.20231219; TART=%1%enc%3AaRoBz%2F%2BZBUxOpx7g77oKOdMI5v0JQ%2FHvbQW0kjul4z5w4gRQ9Jad87AYGr%2FhOj62rt3bdmzG49c%3D; TASID=B7736B7974A046EB869DEDF83EFB5A25; PAC=ADhASJ-SlV7ErVmKDhPfHn_8kN7xMgWETj2ltnSs1c2Klj5MNiSauQyLOeSrBRzAhDDwE7cT5Cu18RX8Toz-vdhfZVnqcYnixPIjYPxG9fUAXAwpXKlL4xSIrxYFOzWyS3CQwBj9zosmd1DyMGzNTw27d-iEzUfabmJQUAAsSm2Hkeoyya4_nqdNchU05tyCWqErJg_HMf9meilqX-7fbUe3UegvcKRxG725Is-korxC; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1*RY.2023*RM.12*RD.20*RH.20*RG.2; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; pbjs_sharedId=922875ad-ef39-4602-b1a3-65cae8f083c1; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; _li_dcdm_c=.tripadvisor.co.id; _lc2_fpi=e3d9117eacb0--01hj112br4a8secqbx2nsfdw8q; _lc2_fpi_meta=%7B%22w%22%3A1702989213444%7D; _ga=GA1.1.1955129227.1702989214; __gads=ID=5ec7cbf724913a72:T=1702989214:RT=1702989214:S=ALNI_MbYUYynUsTEPy-ctZrIc5nx5CApeg; _lr_sampling_rate=100; _lr_retry_request=true; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID%22%3A%220ee2a1ae-b246-4f45-8c52-85529046e1bb%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-19T12%3A33%3A40%22%7D; pbjs_unifiedID_cst=zix7LPQsHA%3D%3D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoajExMmJyNGE4c2VjcWJ4Mm5zZmR3OHEmcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi=%7B%7D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoajExMmJyNGE4c2VjcWJ4Mm5zZmR3OHEmcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi_meta=%7B%22w%22%3A1702989221075%2C%22e%22%3A1702992820000%7D; pbjs_li_nonid=%7B%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; ab.storage.deviceId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22fa636772-6f10-8a80-2391-096d6340da5f%22%2C%22c%22%3A1702989213823%2C%22l%22%3A1702989285410%7D; SRT=%1%enc%3AaRoBz%2F%2BZBUxOpx7g77oKOdMI5v0JQ%2FHvbQW0kjul4z5w4gRQ9Jad87AYGr%2FhOj62rt3bdmzG49c%3D; TAReturnTo=%1%%2FRestaurant_Review-g294229-d2170823-Reviews-Table8-Jakarta_Java.html; roybatty=TNI1625!ADIQyi1v9hFDYop71IsAMtPDoRFbAETCWH0De32Phf66KLRiY8L2IyBQe271cJL6MWgdQgShdlaLdy91MUdNPv5v74cYQK%2FQaEh2Dm1Z3zA%2F2fujSC18aafLJYN33rZmlSwC16qp2LfhWu37hTwSe%2FpkGk6F9SQQ8NZDYlkhMz0RrIbDcuiGkg7cbwp5Pyajpg%3D%3D%2C1; ab.storage.sessionId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22349b4ba7-422f-f527-22dd-14a8906abbe1%22%2C%22e%22%3A1702989427359%2C%22c%22%3A1702989285409%2C%22l%22%3A1702989367359%7D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Dec+19+2023+19%3A36%3A11+GMT%2B0700+(Western+Indonesia+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=acc56f53-bdd9-4e2b-828d-f6c950106d00&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _ga_QX0Q50ZC9P=GS1.1.1702989213.1.1.1702989371.56.0.0; TASession=V2ID.B7736B7974A046EB869DEDF83EFB5A25*SQ.35*LS.ImproveListing*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.in*FA.1*DF.0*TRA.true*LD.294229*EAU._; TAUD=LA-1702989211239-1*RDD-1-2023_12_20*RD-156772-2023_12_20.2170823*LG-198195-2.1.F.*LD-198196-.....; datadome=6v4qIB22za9F~04RY5Qx8iys6T5nf1JWXllS1q9cqPSNpBEwmN1XAqfo~R6JIMUZ3NcxWG2NszoyNsD5lrWGSh59to4D_YGT_mD6o9amLYQBSwSDS52DnazCGzbGYEWv; __vt=Cv_M2AiZ1XKsyl0-ABQCCQPEFUluRFmojcP0P3EgGiovK0Q-_yAAMWuZ1ll946RS23Xk4oHqOJfTFGTCeLj1KQPvWHl4s-20vt_MJJ9JncFWTmO9KTODelhzVlTbcOEmwqmlAyM8LxroKpf4cVBJZAgLtg',
    'origin': 'https://www.tripadvisor.co.id',
    'pragma': 'no-cache',
    'referer': 'https://www.tripadvisor.co.id/Restaurants-g294229-oa30-Jakarta_Java.html',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.110", "Google Chrome";v="120.0.6099.110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-requested-by': '893c5c2aa950501bc7884deada354bd7882eec79e257ba789fff2447731dfa11'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.status_code)
    resto = json.loads(response.text)[4]['data']['response']['restaurants']
    urls = ['https://www.tripadvisor.co.id'+i['detailPageRoute']['url'] for i in resto]
    # print(urls)
    return urls


def get_contact(param,text):
    if param == 'website':
        pattern = r'"website":"([^"]+)",'
    elif param == 'email':
        pattern = r'"email":"([^"]+)",'
    elif param == 'phone':
        pattern = r'"phone":"([^"]+)",'
    else:
        pass

    match = re.search(pattern, text)

    if match:
        result = match.group(1)
        return result

async def fetch(url, session):
    
    headers = {
        'authority': 'www.tripadvisor.co.id',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'TADCID=Vq9aj1WlhE6EymbqABQCCKy0j55CTpGVsECjuwJMq3qTrPU6VVmo8J5hhJYmtqDonXT5Az2MLZMAGf8-Q2SOFjVi8ogcIf8EFMU; TASameSite=1; TAUnique=%1%enc%3AcCMdDwVAlW%2BqXkb1GXX06Nf%2FMcZVRT9aEB5x1ze%2BACCdvEegZdk0%2Fcrma5Rso96sNox8JbUSTxk%3D; __vt=GzK_ZbhEjz2IrlZrABQCCQPEFUluRFmojcP0P3EgGipxTPZI_Wxh7d0bFuAu_-AAO4njPanwu0trw2llOPIwkXe_-nVotr5Ool2p_ixeCdRPB8Fsi0C_Kh7P8Hvcu0xG6hfAD9wScEYXikvvDBCI-C-7kQ; TASSK=enc%3AAAlSbzY4zFDxD7g2%2BAqpIvU9uMx4Ru%2BWB1kHOZuHb%2BSZvy6yf1RCvQS9SJmIbZp5B0z2BTqF2aaa64PU3SuzNLQL0grTaL2kYZX%2Bj8Boy%2FX%2BrM7CCl%2Be9jYZyAqsf5stkw%3D%3D; SRT=TART_SYNC; ServerPool=A; PMC=V2*MS.90*MD.20231231*LD.20231231; TART=%1%enc%3AaRoBz%2F%2BZBUxy%2BFFQJFh6zLtgZhV%2FmbR9T7w60wlPhI3sBpFHOxTCDfcHUU7X2OtHESYSBoCa3%2Fw%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TASID=22667C9B11CA4B99A17EAC0F07D69557; PAC=ACGdeyHYmVLoMjbjrthIWEW7xd6MJyGnInPr7jE6KKQE7a9kbz3qGpgjMGk5cyX8kvOTlAsacaZg86aKNLRVXdaOmmaIG4bCXXB2-BQOYT2WkUN4z9WGMdsJ8MWKmBRWrz5-axMQo3BQmznWWUEBwv_xWiTAZrtmmlS_I_2RoBSp; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; _ga=GA1.1.1530178142.1704005727; WLRedir=requested; pbjs_sharedId=9f0202f7-427c-4f94-a7c3-a5d337cbff29; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; _li_dcdm_c=.tripadvisor.co.id; _lc2_fpi=e3d9117eacb0--01hjzafy49dj1vqdj33ejn1tw2; _lc2_fpi_meta=%7B%22w%22%3A1704005728393%7D; __gads=ID=8cc33b01e4835eb1:T=1704005732:RT=1704005732:S=ALNI_MbosB7jBRLBbjkcVDQDEPCRfaPg7g; __gpi=UID=00000cccac88f24d:T=1704005732:RT=1704005732:S=ALNI_MajbIBPRCGgiFEvexc_rWfH2-0oiw; _lr_sampling_rate=100; _lr_retry_request=true; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID%22%3A%226e3bb257-4a68-4d6a-af68-501f97bf8757%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-31T06%3A55%3A48%22%7D; pbjs_unifiedID_cst=zix7LPQsHA%3D%3D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoanphZnk0OWRqMXZxZGozM2VqbjF0dzImcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi=%7B%7D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoanphZnk0OWRqMXZxZGozM2VqbjF0dzImcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi_meta=%7B%22w%22%3A1704005746176%2C%22e%22%3A1704009348000%7D; pbjs_li_nonid=%7B%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; TAReturnTo=%1%%2FRestaurant_Review-g294229-d12958497-Reviews-Catappa_Restaurant-Jakarta_Java.html; roybatty=TNI1625!AP%2FTCBc3Iv8FMar%2FLEm7fMVx2X%2Bk3iy7GmEB7fmAxDS22JT4bz0JMpGJ%2FuG8tf58cRKroPVuxpeWUxr5RJZtonDhRTGyPQ3FTmPiNzCG7Do1ueu1ZUd4vUYg5b%2F7gLJSGYW21OsDdezSJf4sqecMEHqNr9%2BLCQmbcT85gwN5%2FcybNg3tMgepwOETdw5Z7xFy%2Bg%3D%3D%2C1; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+31+2023+13%3A55%3A50+GMT%2B0700+(Western+Indonesia+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0ac5031d-ea10-4eb5-b573-c29a2e635739&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; TASession=V2ID.22667C9B11CA4B99A17EAC0F07D69557*SQ.11*LS.DemandLoadAjax*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.in*FA.1*DF.0*TRA.true*LD.12958497*EAU._; TAUD=LA-1704005728249-1*RDD-1-2023_12_31*LG-26391-2.1.F.*LD-26392-.....; _ga_QX0Q50ZC9P=GS1.1.1704005727.1.1.1704005753.34.0.0',
        'pragma': 'no-cache',
        'referer': url,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    

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
            data = parse(soup,url)
            return data
    except Exception as e:
        # print(e)
        return {
            'resto': None,
            'culinary':None,
            'street':None,
            'area':None,
            'phone':None,
            'email':None,
            'website':None,
            'keyword':None,
            'url':url
            }
        
        # return (url, 'ERROR', str(e))

async def run(url_list):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
    return responses

def parse(soup,url):
    dom = etree.HTML(str(soup)) 
    try:
        resto = soup.find('h1',{'class':'HjBfq'}).text.strip()

        culinary_list = soup.find('span',{'class':'DsyBj DxyfE'}).find_all('a')[1:]
        culinary = [i.text for i in culinary_list]
    except:
        culinary = None
        resto = None

    try:

        
        maps_sec = soup.find_all('div',{'class':'YDAvY R2 F1 e k'})[-1]
        area = maps_sec.find('span',{'class':'yEWoV OkcwQ'}).find('div').text
    except:
        area = None
    try:
        # street = maps_sec.find('span',{'class':'yEWoV'}).text.replace('\\n','').strip()

        street = dom.xpath('/html/body/div[2]/div[1]/div/div[4]/div/div/div[3]/span[1]/span/a')[0].text
    except:
        street = None
    try:
        scrip = soup.find_all('script')
        script_ = [i for i in scrip if 'window.__WEB_CONTEXT__' in i.text]
        website = get_contact('website',script_[0].text)
        email = get_contact('email',script_[0].text)
        phone = get_contact('phone',script_[0].text)
    except:
        email = None
        website = None
        phone = None

    try:
        keyword = soup.find('div',{'class':'BMlpu'}).find_all('div',{'class':'SrqKb'})
        keyword = [i.text for i in keyword]
    except:
        keyword = None

    result = {
        'resto': resto,
        'culinary':culinary,
        'street':street,
        'area':area,
        'phone':phone,
        'email':email,
        'website':website,
        'keyword':keyword,
        'url':url
    }
    return result

def scrape_urls(url_list):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    task = asyncio.ensure_future(run(url_list))
    loop.run_until_complete(task)
    result = task.result().result()
    
    return result


async def single_req(url):

    headers = {
        'authority': 'www.tripadvisor.co.id',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'TADCID=Vq9aj1WlhE6EymbqABQCCKy0j55CTpGVsECjuwJMq3qTrPU6VVmo8J5hhJYmtqDonXT5Az2MLZMAGf8-Q2SOFjVi8ogcIf8EFMU; TASameSite=1; TAUnique=%1%enc%3AcCMdDwVAlW%2BqXkb1GXX06Nf%2FMcZVRT9aEB5x1ze%2BACCdvEegZdk0%2Fcrma5Rso96sNox8JbUSTxk%3D; __vt=GzK_ZbhEjz2IrlZrABQCCQPEFUluRFmojcP0P3EgGipxTPZI_Wxh7d0bFuAu_-AAO4njPanwu0trw2llOPIwkXe_-nVotr5Ool2p_ixeCdRPB8Fsi0C_Kh7P8Hvcu0xG6hfAD9wScEYXikvvDBCI-C-7kQ; TASSK=enc%3AAAlSbzY4zFDxD7g2%2BAqpIvU9uMx4Ru%2BWB1kHOZuHb%2BSZvy6yf1RCvQS9SJmIbZp5B0z2BTqF2aaa64PU3SuzNLQL0grTaL2kYZX%2Bj8Boy%2FX%2BrM7CCl%2Be9jYZyAqsf5stkw%3D%3D; SRT=TART_SYNC; ServerPool=A; PMC=V2*MS.90*MD.20231231*LD.20231231; TART=%1%enc%3AaRoBz%2F%2BZBUxy%2BFFQJFh6zLtgZhV%2FmbR9T7w60wlPhI3sBpFHOxTCDfcHUU7X2OtHESYSBoCa3%2Fw%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TASID=22667C9B11CA4B99A17EAC0F07D69557; PAC=ACGdeyHYmVLoMjbjrthIWEW7xd6MJyGnInPr7jE6KKQE7a9kbz3qGpgjMGk5cyX8kvOTlAsacaZg86aKNLRVXdaOmmaIG4bCXXB2-BQOYT2WkUN4z9WGMdsJ8MWKmBRWrz5-axMQo3BQmznWWUEBwv_xWiTAZrtmmlS_I_2RoBSp; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; _ga=GA1.1.1530178142.1704005727; WLRedir=requested; pbjs_sharedId=9f0202f7-427c-4f94-a7c3-a5d337cbff29; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; _li_dcdm_c=.tripadvisor.co.id; _lc2_fpi=e3d9117eacb0--01hjzafy49dj1vqdj33ejn1tw2; _lc2_fpi_meta=%7B%22w%22%3A1704005728393%7D; __gads=ID=8cc33b01e4835eb1:T=1704005732:RT=1704005732:S=ALNI_MbosB7jBRLBbjkcVDQDEPCRfaPg7g; __gpi=UID=00000cccac88f24d:T=1704005732:RT=1704005732:S=ALNI_MajbIBPRCGgiFEvexc_rWfH2-0oiw; _lr_sampling_rate=100; _lr_retry_request=true; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID%22%3A%226e3bb257-4a68-4d6a-af68-501f97bf8757%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-31T06%3A55%3A48%22%7D; pbjs_unifiedID_cst=zix7LPQsHA%3D%3D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoanphZnk0OWRqMXZxZGozM2VqbjF0dzImcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi=%7B%7D; __li_idex_cache2_InByZWJpZC82NDQzOT9kdWlkPWUzZDkxMTdlYWNiMC0tMDFoanphZnk0OWRqMXZxZGozM2VqbjF0dzImcmVzb2x2ZT1ub25JZCZyZXNvbHZlPW1hZ25pdGUi_meta=%7B%22w%22%3A1704005746176%2C%22e%22%3A1704009348000%7D; pbjs_li_nonid=%7B%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; TAReturnTo=%1%%2FRestaurant_Review-g294229-d12958497-Reviews-Catappa_Restaurant-Jakarta_Java.html; roybatty=TNI1625!AP%2FTCBc3Iv8FMar%2FLEm7fMVx2X%2Bk3iy7GmEB7fmAxDS22JT4bz0JMpGJ%2FuG8tf58cRKroPVuxpeWUxr5RJZtonDhRTGyPQ3FTmPiNzCG7Do1ueu1ZUd4vUYg5b%2F7gLJSGYW21OsDdezSJf4sqecMEHqNr9%2BLCQmbcT85gwN5%2FcybNg3tMgepwOETdw5Z7xFy%2Bg%3D%3D%2C1; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+31+2023+13%3A55%3A50+GMT%2B0700+(Western+Indonesia+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0ac5031d-ea10-4eb5-b573-c29a2e635739&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; TASession=V2ID.22667C9B11CA4B99A17EAC0F07D69557*SQ.11*LS.DemandLoadAjax*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.in*FA.1*DF.0*TRA.true*LD.12958497*EAU._; TAUD=LA-1704005728249-1*RDD-1-2023_12_31*LG-26391-2.1.F.*LD-26392-.....; _ga_QX0Q50ZC9P=GS1.1.1704005727.1.1.1704005753.34.0.0',
        'pragma': 'no-cache',
        'referer': url,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                headers=headers, 
                                ssl = False, 
                                timeout = aiohttp.ClientTimeout(
                                    total=None, 
                                    sock_connect = 20, 
                                    sock_read = 20
                                )) as response:

                print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])

                html = await response.text()
                # with open("yourhtmlfile.html", "w", encoding='utf-8') as file:
                #     file.write(html)
                soup = BeautifulSoup(html, 'html.parser')
                
                data = parse(soup,url)
                
                return data
    except Exception as e:
        print(e)
        



def putDataRecords(data,table):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    columns = ', '.join(data.keys())
    values_template = ', '.join(['%s' for _ in data.values()])
    insert_query = f'INSERT INTO {table} ({columns}) VALUES ({values_template})'
    
    cursor.execute(insert_query, tuple(data.values()))

    conn.commit()
    conn.close()

def putUpdateLocation(loc,page):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)

    cursor = conn.cursor()

    update_query = "UPDATE location SET page = %s WHERE url = %s"

    cursor.execute(update_query, (page, loc))

    conn.commit()
    conn.close()

def doneLocation(loc):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)

    cursor = conn.cursor()

    update_query = "UPDATE location SET status = %s WHERE url = %s"

    cursor.execute(update_query, ('DONE',loc,))

    conn.commit()
    conn.close()

def getNoneRec(table):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    select_query = f"SELECT * FROM {table} WHERE resto IS NULL ORDER BY RANDOM() LIMIT 10"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    rows = cursor.fetchall()
    urls = []
    for i in rows:
        urls.append(i[-2])

    conn.close()
    return urls

def updateRec(table,url,data):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    update_query = f"UPDATE {table} SET "
    update_query += ', '.join([f"{column} = %s" for column in data.keys()])
    update_query += f" WHERE url = %s"

    # Execute the update query
    cursor.execute(update_query, tuple(data.values()) + (url,))

    conn.commit()
    conn.close()

def checkNullRec():
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = 'SELECT COUNT(*) FROM public.records WHERE resto IS NULL'
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows[0][0]

def getStreetNull():
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    select_query = f"SELECT * FROM records WHERE street IS NULL ORDER BY RANDOM() LIMIT 20"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    rows = cursor.fetchall()
    urls = []
    for i in rows:
        urls.append(i[-2])

    conn.close()
    return urls


def updateStreet(table,data):
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    update_query = f"UPDATE {table} SET "
    update_query += ' street = %s '
    update_query += f" WHERE url = %s"

    # Execute the update query
    cursor.execute(update_query, (data['street'],data['url'],))

    conn.commit()
    conn.close()

def checkNullStreet():
    db_params = {
        'host': 'localhost',
        'database': 'resto',
        'user': 'postgres',
        'password': 'admin',
        'port': '5432',  
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = 'SELECT COUNT(*) FROM public.records WHERE street IS NULL'
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows[0][0]