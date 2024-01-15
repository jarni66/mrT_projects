from function import *
import psycopg2


def main():
    with open('OUTPUT/location_urls.json') as f:
        loc_urls = json.load(f)
    for loc_url in loc_urls[45:]:
        loc_name = loc_url.split('-')[-1].split('.')[0]
        page = 0
        stats = True
        while stats == True:
            try:
                url_list = get_resto_urls(page,loc_url)
                results = scrape_urls(url_list)
                for data in results:
                    putDataRecords(data, 'records')
                
                print(f"{loc_name} page {page} item {len(results)}")

                putUpdateLocation(loc_url,page)
                page += 1
                if len(url_list) == 0:
                    stats = False
            except:
                print(f"FAIL {loc_name} page {page} item {len(results)}")
                page += 1
                if page >100:
                    stats = False

        doneLocation(loc_url)
        

def main_recover():
    urls = getNoneRec('records')
    datas = scrape_urls(urls)
    count_update = 0
    nulls = checkNullRec()
    for data in datas:
        if data['resto'] != None:
            try:
                updateRec('records',data['url'],data)
                count_update += 1
            except:
                count_update += 1
    print(f"UPDATED : {count_update} DATANULLS : {nulls}")


def main_recoverStreet():
    urls = getStreetNull()
    datas = scrape_urls(urls)
    count_update = 0
    nulls = checkNullStreet()
    for data in datas:
        if data['street'] != None:
            try:
                updateStreet('records',data)
                count_update += 1
            except:
                count_update += 1
    print(f"UPDATED : {count_update} DATANULLS : {nulls}")


reco = 0
while True:
    main_recoverStreet()
    reco += 1
    if reco == 1000:
        break
    
# test = getStreetNull()

# print(test)
# url = 'https://www.tripadvisor.co.id/Restaurant_Review-g294229-d4233517-Reviews-Fajar_International_Restaurant-Jakarta_Java.html'

# test = asyncio.run(single_req(url))

# print(test)
# urls = getStreetNull()
# datas = scrape_urls(urls)
# print(datas)