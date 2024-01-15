import requests
import json
import time
import random
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import concurrent.futures
import threading
import aiohttp
import asyncio
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium import webdriver
import asyncio
from requests_html import AsyncHTMLSession

def load_json(name):
    with open(name) as f:
        out = json.load(f)
    return out
def to_json(name,data):
    with open(name, 'w') as f:
        json.dump(data, f)

def get_agent_page(page):

    url = "https://www.rumah123.com/directory-pages-api/agent-page/search-agents/"

    payload = json.dumps({
        "searchAgentFilter": {
            "keyword": "",
            "organizationUuid": "",
            "uuid": "",
            "languages": [],
            "specialists": [],
            "locations": []
        },
        "searchAgentSort": "OLDEST",
        "page": page
    })
    headers = {
        'authority': 'www.rumah123.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ko;q=0.8,id;q=0.7,de;q=0.6,de-CH;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'is-new-login=false; _gcl_au=1.1.1608358082.1700211082; _gid=GA1.2.1624559848.1700211085; ajs_anonymous_id=47e46d0b-8156-4705-b9bd-6c89abc89fb8; enquiry_data={"name":"","phoneNumber":"","requestId":"","isVerified":false}; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22EwMv3geYGZpECi4gM2I2%22%7D; _fbp=fb.1.1700211108702.1055324155; _tt_enable_cookie=1; _ttp=bGsafXdIQUM6R9Ma4yGsVlfxBuy; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI3ZTRiZDBlZS0zOGM3LTRjYjQtOTFlNi0yZTNiZTIxMzViMGQifQ==; __stbpnenable=MQ==; __stdf=MA==; bxSesT=MTcwMDIxMTExMDAzMg%3D%3D; bxSesC=MTcwMDIxMTExMDAzMg%3D%3D; boxx_token_id=N2U0YmQwZWUtMzhjNy00Y2I0LTkxZTYtMmUzYmUyMTM1YjBk; __sts=eyJzaWQiOjE3MDAyMTExMDkxMjIsInR4IjoxNzAwMjExMTE4NTMwLCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ydW1haDEyMy5jb20lMkZhZ2VuLXByb3BlcnRpJTJGIiwicGV0IjoxNzAwMjExMTE4NTMwLCJzZXQiOjE3MDAyMTExMDkxMjIsInBVcmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ydW1haDEyMy5jb20lMkZhZ2VuLXByb3BlcnRpJTJGJTNGc29ydCUzRE5FV19MSVNUSU5HJTI2YWdlbnRfdHlwZSUzRElOREVQRU5ERU5UIiwicFBldCI6MTcwMDIxMTEwOTEyMiwicFR4IjoxNzAwMjExMTA5MTIyfQ==; bxCacheInit=MQ%3D%3D; bxSegDetail=eyJieFNlc1QiOjE3MDAyMTExMTAwMzIsInVzZXJUeXBlIjoibmV3IiwidXNlclJhbmRvbSI6MC4xMTkyOTU2MDI0MjI5ODk4NywicHJ2TXYiOiI2OTUiLCJwdWJNdiI6ImJveHgiLCJ1c2VyU2VnIjoiX2RlZmF1bHQiLCJtb2RlbFNlZyI6ImJveHhfX2RlZmF1bHQifQ%3D%3D; __stat=IkJMT0NLIg==; _gat_UA-34838320-19=1; _gat_UA-34838320-25=1; _ga=GA1.1.1200101250.1700211084; _ga_BTHL9PR2SF=GS1.2.1700211084.1.1.1700211158.0.0.0; __stgeo=ImRlbmllZCI=; _cc_id=c6410eae8ae380aa632c53f2793283fc; panoramaId_expiry=1700297582970; panoramaId=e1282a57d3185a91fb46868c36f1a9fb927a4213d8b095bee2d945130ab479bc; panoramaIdType=panoDevice; cto_bundle=kKFjoV96MWdWMXA0WHQ0Um14QTFNJTJGWHlqeEJzRFloSkJwbUVxUVJpeUc1NDZLdHR1QlhRU0xJelB6c2d4MHJkZEclMkI0Yll5JTJCdVd5d3ZRZyUyRlAzUVNPJTJGUCUyQmRWa3g0Q014NXByMW83YW92WUpEdUp4MHo1RnhWYmMxM1olMkZNbXZYN3N6SDd0YXFEbHFhcTB4WGljQnRlRU9BQXBQcWVKUE9wcEglMkZhJTJGbkVxSVNkZ0xMM0klM0Q; _ga_D5V06TRY2R=GS1.1.1700211084.1.1.1700211187.28.0.0; _ga_Z36X54E7Z5=GS1.1.1700211084.1.1.1700211194.0.0.0',
        'origin': 'https://www.rumah123.com',
        'pragma': 'no-cache',
        'referer': 'https://www.rumah123.com/agen-properti/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    data = json.loads(response.text)['Users']
    agents_head = data['users']
    # total_agent = data['pageInfo']['total']
    time.sleep(random.uniform(1,2))
    return agents_head
    # return response.text

def get_listing_numbers(uuid):
    url = "https://www.rumah123.com/directory-pages-api/core-service/find-properties-by-filter/"

    payload = json.dumps({
    "userRequest": {
        "agents": uuid,
        "priceTypes": [
        0,
        1
        ],
        "propertyTypes": [
        15,
        2,
        4,
        5,
        7,
        8,
        11
        ],
        "locations": [],
        "minPrice": 0,
        "maxPrice": 0,
        "status": [
        "ACTIVE",
        "SOLD_RENTED"
        ],
        "transactedIncluded": True,
        "paginationRequest": {
        "page": 1,
        "pageSize": 12
        },
        "query": ""
    },
    "query": "\n\t\t\tquery\n\t\t\t\tFindPropertiesByFilters ($request: FindPropertiesByFiltersRequest) {\n\t\t\t\t\tFindPropertiesByFilters (request: $request) {\n\t\t\t\t\t\tpaginationResponse {\n\t\t\t\t\t\t\tpage\n\t\t\t\t\t\t\tpageSize\n\t\t\t\t\t\t\ttotalCount\n\t\t\t\t\t\t\tpageCount\n\t\t\t\t\t\t}\n\t\t\t\t\t\tproperties {\n\t\t\t\t\t\t\ttitle\n\t\t\t\t\t\t\tpriceType {\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tprice {\n\t\t\t\t\t\t\t\tdisplay\n\t\t\t\t\t\t\t\toffer\n\t\t\t\t\t\t\t\tminValue\n\t\t\t\t\t\t\t\tmaxValue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\turl\n\t\t\t\t\t\t\tagent {\n\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\torganization {\n\t\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tsubscription {\n\t\t\t\t\t\t\t\t\ttype {\n\t\t\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\t\t\tlabel\n\t\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\toriginId\n\t\t\t\t\t\t\t\tcontacts {\n\t\t\t\t\t\t\t\t\ttype\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocation {\n\t\t\t\t\t\t\t\ttext\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocationPin {\n\t\t\t\t\t\t\t\tlatitude\n\t\t\t\t\t\t\t\tlongitude\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\toriginId {\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tmedias {\n\t\t\t\t\t\t\t\tmediaType\n\t\t\t\t\t\t\t\tmediaInfo {\n\t\t\t\t\t\t\t\t\tformatUrl\n\t\t\t\t\t\t\t\t\ttitle\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tpropertyType {\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tspecialFlag {\n                                isPrimaryProject\n\t\t\t\t\t\t\t\tisSubunit\n                            }\n\t\t\t\t\t\t\tprimaryProject {\n\t\t\t\t\t\t\t\tprojectType\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocation {\n\t\t\t\t\t\t\t\ttext\n\t\t\t\t\t\t\t\tlevel\n\t\t\t\t\t\t\t\tcity {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tdistrict {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tprovince {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\ttime {\n\t\t\t\t\t\t\t\tupdated\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tattributes {\n\t\t\t\t\t\t\t\tlandSize {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbuildingSize {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbedrooms {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbathrooms {\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tcarports {\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tsubscriptionTierId\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t"
    })

    headers = {
    'authority': 'www.rumah123.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'enquiry_data={"name":"","phoneNumber":"","requestId":"","isVerified":false}; _gcl_au=1.1.326402609.1700359334; _gid=GA1.2.27825802.1700359334; _fbp=fb.1.1700359334395.652378330; __sts=eyJzaWQiOjE3MDAzNTkzMzQ0NDgsInR4IjoxNzAwMzU5MzM0NDQ4LCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ydW1haDEyMy5jb20lMkZhZ2VuLXByb3BlcnRpJTJGJTNGJTI2c29ydCUzRE5FV19MSVNUSU5HJTI2IiwicGV0IjoxNzAwMzU5MzM0NDQ4LCJzZXQiOjE3MDAzNTkzMzQ0NDh9; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiJhOWE1OTNkYi05MDYzLTRjNTYtOGM3YS02N2UzMmRjNGIzNGUifQ==; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22eS3kj9Tcs3jOXMv7NnR5%22%7D; __stgeo=IjEi; __stbpnenable=MQ==; _tt_enable_cookie=1; _ttp=NygvljWAHaMnV-cn1uW9ePjvZZa; __stat=IkJMT0NLIg==; bxSesT=MTcwMDM1OTMzNDk1Nw%3D%3D; bxSesC=MTcwMDM1OTMzNDk1Nw%3D%3D; boxx_token_id=YTlhNTkzZGItOTA2My00YzU2LThjN2EtNjdlMzJkYzRiMzRl; __stdf=MA==; bxCacheInit=MQ%3D%3D; bxSegDetail=eyJieFNlc1QiOjE3MDAzNTkzMzQ5NTcsInVzZXJUeXBlIjoibmV3IiwidXNlclJhbmRvbSI6MC44MTA5Nzg5NjEyNTI5NzI1LCJwcnZNdiI6IjY5NSIsInB1Yk12IjoiYm94eCIsInVzZXJTZWciOiJfZGVmYXVsdCIsIm1vZGVsU2VnIjoiYm94eF9fZGVmYXVsdCJ9; ajs_anonymous_id=f4e3562d-dde5-49be-bf0e-ec4993ec396d; _cc_id=a6829610bc6f253d892ffdfd3385a694; panoramaId_expiry=1700445795798; cto_bundle=_mbiMV9JaTNKWmRTJTJGNk5xbVlHTTFlWjMyd3dCbU5lMUg5WnhBYUMyVkNaZ3NTalpOT0lrY2FvWnpvNkFiaE4lMkZPQnFGOVRZWUZ3REs1WktRMDhoUXpKVWtOZFBnT2NqWWlLc0hqMyUyQmdXdkslMkJoVURBbVVxQTJXT0RtR2Jtc29DQ1FLdDFJ; _ga=GA1.2.124465363.1700359334; _ga_BTHL9PR2SF=GS1.2.1700359334.1.1.1700359522.0.0.0; _ga_D5V06TRY2R=GS1.1.1700359334.1.1.1700359734.60.0.0; _ga_Z36X54E7Z5=GS1.1.1700359334.1.1.1700359736.0.0.0',
    'origin': 'https://www.rumah123.com',
    'pragma': 'no-cache',
    'referer': 'https://www.rumah123.com/agen-properti/independent-property-agent/ripan-afrian-1869137/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    all_item = data['paginationResponse']['totalCount']
    return all_item

def get_agent_listing(agent_page):
    uuid = agent_page['uuid']
    all_item = get_listing_numbers(uuid)

    headers = {
    'authority': 'www.rumah123.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'enquiry_data={"name":"","phoneNumber":"","requestId":"","isVerified":false}; _gcl_au=1.1.326402609.1700359334; _gid=GA1.2.27825802.1700359334; _fbp=fb.1.1700359334395.652378330; __sts=eyJzaWQiOjE3MDAzNTkzMzQ0NDgsInR4IjoxNzAwMzU5MzM0NDQ4LCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ydW1haDEyMy5jb20lMkZhZ2VuLXByb3BlcnRpJTJGJTNGJTI2c29ydCUzRE5FV19MSVNUSU5HJTI2IiwicGV0IjoxNzAwMzU5MzM0NDQ4LCJzZXQiOjE3MDAzNTkzMzQ0NDh9; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiJhOWE1OTNkYi05MDYzLTRjNTYtOGM3YS02N2UzMmRjNGIzNGUifQ==; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22eS3kj9Tcs3jOXMv7NnR5%22%7D; __stgeo=IjEi; __stbpnenable=MQ==; _tt_enable_cookie=1; _ttp=NygvljWAHaMnV-cn1uW9ePjvZZa; __stat=IkJMT0NLIg==; bxSesT=MTcwMDM1OTMzNDk1Nw%3D%3D; bxSesC=MTcwMDM1OTMzNDk1Nw%3D%3D; boxx_token_id=YTlhNTkzZGItOTA2My00YzU2LThjN2EtNjdlMzJkYzRiMzRl; __stdf=MA==; bxCacheInit=MQ%3D%3D; bxSegDetail=eyJieFNlc1QiOjE3MDAzNTkzMzQ5NTcsInVzZXJUeXBlIjoibmV3IiwidXNlclJhbmRvbSI6MC44MTA5Nzg5NjEyNTI5NzI1LCJwcnZNdiI6IjY5NSIsInB1Yk12IjoiYm94eCIsInVzZXJTZWciOiJfZGVmYXVsdCIsIm1vZGVsU2VnIjoiYm94eF9fZGVmYXVsdCJ9; ajs_anonymous_id=f4e3562d-dde5-49be-bf0e-ec4993ec396d; _cc_id=a6829610bc6f253d892ffdfd3385a694; panoramaId_expiry=1700445795798; cto_bundle=_mbiMV9JaTNKWmRTJTJGNk5xbVlHTTFlWjMyd3dCbU5lMUg5WnhBYUMyVkNaZ3NTalpOT0lrY2FvWnpvNkFiaE4lMkZPQnFGOVRZWUZ3REs1WktRMDhoUXpKVWtOZFBnT2NqWWlLc0hqMyUyQmdXdkslMkJoVURBbVVxQTJXT0RtR2Jtc29DQ1FLdDFJ; _ga=GA1.2.124465363.1700359334; _ga_BTHL9PR2SF=GS1.2.1700359334.1.1.1700359522.0.0.0; _ga_D5V06TRY2R=GS1.1.1700359334.1.1.1700359734.60.0.0; _ga_Z36X54E7Z5=GS1.1.1700359334.1.1.1700359736.0.0.0',
    'origin': 'https://www.rumah123.com',
    'pragma': 'no-cache',
    'referer': 'https://www.rumah123.com/agen-properti/independent-property-agent/ripan-afrian-1869137/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    payload = json.dumps({
    "userRequest": {
        "agents": uuid,
        "priceTypes": [
        0,
        1
        ],
        "propertyTypes": [
        15,
        2,
        4,
        5,
        7,
        8,
        11
        ],
        "locations": [],
        "minPrice": 0,
        "maxPrice": 0,
        "status": [
        "ACTIVE",
        "SOLD_RENTED"
        ],
        "transactedIncluded": True,
        "paginationRequest": {
        "page": 1,
        "pageSize": all_item
        },
        "query": ""
    },
    "query": "\n\t\t\tquery\n\t\t\t\tFindPropertiesByFilters ($request: FindPropertiesByFiltersRequest) {\n\t\t\t\t\tFindPropertiesByFilters (request: $request) {\n\t\t\t\t\t\tpaginationResponse {\n\t\t\t\t\t\t\tpage\n\t\t\t\t\t\t\tpageSize\n\t\t\t\t\t\t\ttotalCount\n\t\t\t\t\t\t\tpageCount\n\t\t\t\t\t\t}\n\t\t\t\t\t\tproperties {\n\t\t\t\t\t\t\ttitle\n\t\t\t\t\t\t\tpriceType {\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tprice {\n\t\t\t\t\t\t\t\tdisplay\n\t\t\t\t\t\t\t\toffer\n\t\t\t\t\t\t\t\tminValue\n\t\t\t\t\t\t\t\tmaxValue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\turl\n\t\t\t\t\t\t\tagent {\n\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\torganization {\n\t\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tsubscription {\n\t\t\t\t\t\t\t\t\ttype {\n\t\t\t\t\t\t\t\t\t\tname\n\t\t\t\t\t\t\t\t\t\tlabel\n\t\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\toriginId\n\t\t\t\t\t\t\t\tcontacts {\n\t\t\t\t\t\t\t\t\ttype\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocation {\n\t\t\t\t\t\t\t\ttext\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocationPin {\n\t\t\t\t\t\t\t\tlatitude\n\t\t\t\t\t\t\t\tlongitude\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\toriginId {\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tmedias {\n\t\t\t\t\t\t\t\tmediaType\n\t\t\t\t\t\t\t\tmediaInfo {\n\t\t\t\t\t\t\t\t\tformatUrl\n\t\t\t\t\t\t\t\t\ttitle\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tpropertyType {\n\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tspecialFlag {\n                                isPrimaryProject\n\t\t\t\t\t\t\t\tisSubunit\n                            }\n\t\t\t\t\t\t\tprimaryProject {\n\t\t\t\t\t\t\t\tprojectType\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tlocation {\n\t\t\t\t\t\t\t\ttext\n\t\t\t\t\t\t\t\tlevel\n\t\t\t\t\t\t\t\tcity {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tdistrict {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tprovince {\n\t\t\t\t\t\t\t\t  name\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\ttime {\n\t\t\t\t\t\t\t\tupdated\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tattributes {\n\t\t\t\t\t\t\t\tlandSize {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbuildingSize {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbedrooms {\n\t\t\t\t\t\t\t\t  value\n\t\t\t\t\t\t\t\t  formattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tbathrooms {\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tcarports {\n\t\t\t\t\t\t\t\t\tvalue\n\t\t\t\t\t\t\t\t\tformattedValue\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\tsubscriptionTierId\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t"
    })
    url = "https://www.rumah123.com/directory-pages-api/core-service/find-properties-by-filter/"
    
    response = requests.request("POST", url, headers=headers, data=payload)
    datas = []
    try:
        data = json.loads(response.text)['properties']
        # data = json.loads(response.text)
        # return response.text
        
        for listing in data:
            # time.sleep(random.uniform(0.2,0.9))
            try:
                # print(f"{agent_page['name']} {data.index(listing)}/{len(data)}")
                data = get_listing_details(listing)
                datas.append(data)
            except:
                # print(f"{agent_page['name']} {data.index(listing)}/{len(data)} FAIL")
                pass
    except:
        pass
    return datas

def get_images(data):
    images = []
    for med in data['medias']:
        for img in med['mediaInfo']:
            size = '1280x720-1'
            url = img['formatUrl'].replace('{width}x{height}-{scale}',size)
            images.append(url)
    return images

def get_contact(contact, param):
    for i in contact:
        if i['type'] == param:
            return i['value']
    return None

def get_agency(data):
    try:
        agency = data['agent']['organization']['name']
        return agency
    except:
        agency = data['agent']['organization']
        return agency

def get_desc(url):
    time.sleep(random.uniform(1,2))
    
    try:
        
        url_home = 'https://www.rumah123.com'
        url_desc = url_home + url
        session = HTMLSession()
        r = session.get(url_desc)
        if r.status_code == 429:
            time.sleep(int(r.headers['Retry-After']))
        # print(type(r.status_code))
        # try:
        #     print(r.headers['Retry-After'])
        # except:
        #     pass

        # r = await asession.get(url_desc)

        r.html.render()
        rendered_html = r.html.html
        soup = BeautifulSoup(rendered_html, 'html.parser')
        # session.close()

        desc = soup.find('div',{'class':'ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary content-wrapper'}).text
        
    except:
        
        desc = None
    return desc

def get_descUC(url):
    url_home = 'https://www.rumah123.com'

    url = url_home + url
    ua = UserAgent(browsers=['chrome'])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--user-agent={ua.random}")


    driver = uc.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    desc = soup.find('div',{'class':'ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary content-wrapper'}).text
    

    return desc

def get_desc2(url):
    
    asession = AsyncHTMLSession()
    async def get_pythonorg():
        url_home = 'https://www.rumah123.com'
        url_desc = url_home + url
        r = await asession.get(url_desc)
 
        rendered_html = r.html.html
        soup = BeautifulSoup(rendered_html, 'html.parser')

        desc = soup.find('div',{'class':'ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary content-wrapper'}).text

        return desc
    return asession.run(get_pythonorg)[0]



def get_listing_details(listing):
    data = {
        'url': 'https://www.rumah123.com' + listing['url'],
        'title': listing['title'],
        'desc': None,
        'price': listing['price']['offer'],
        'price_tag': listing['price']['display'],
        'address': listing['location']['text'],
        'city': listing['location']['city']['name'],
        'province': listing['location']['province']['name'],
        'propertyCategory': listing['propertyType']['formattedValue'],
        'propertyType': listing['priceType']['formattedValue'],
        'agent_name': listing['agent']['name'],
        'agency': get_agency(listing),
        'agent_url': get_contact(listing['agent']['contacts'],'WEBSITE'),
        'agent_email': get_contact(listing['agent']['contacts'],'EMAIL'),
        'agent_phone': get_contact(listing['agent']['contacts'],'PHONE_NUMBER'),
        'agent_wa': get_contact(listing['agent']['contacts'],'WHATSAPP'),
        'images' : get_images(listing)

    }
    return data


class SafeItemList:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()

    def add_item(self, items):
        with self.lock:
            self.items.append(items)

def process_item(item):
    # Perform some processing on the item
    start_time = time.time()
    processed_item = get_agent_listing(item)

    # Save the processed item safely
    item_name = item['name']
    print(f'process {item_name}')
    end_time = time.time()
    elapsed_time = end_time - start_time

    # print(f"Elapsed time: {elapsed_time} seconds")
    return processed_item


async def description(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url,ssl=False,headers = {'User-agent': 'your bot 0.1'}) as response:
            
            if response.status == 429:
                time.sleep(int(response.headers['Retry-After']))

            time.sleep(random.uniform(1,2))

            html = await response.text()
            try:
                soup = BeautifulSoup(html, 'html.parser')
                desc = soup.find('div',{'class':'ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary content-wrapper'}).text

            except:
                desc = None
        await session.close()
    return desc

