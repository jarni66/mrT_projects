from function import *




def main():
    files = get_folder()
    files.sort()
    last_num = files[-1] + 2
    datas = []
    for page in range(451,1001):
        start_time = time.time()
        page_urls = get_page_listing(page)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            results = list(executor.map(get_listing_details,page_urls))
            datas += results

        if page%50 == 0:
            with open(f'listings_data2/listings_data_{page}.json', 'w') as f:
                json.dump(datas, f)
            datas = []

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"PAGE {page} {round(elapsed_time,2)}")

def main_listing_urls():


    data = []
    a = 1
    b = 101
    pages = list(range(a,b))
    status = True
    while status == True:

        start_time = time.time()

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(run(pages))
        loop.run_until_complete(task)
        result = task.result().result()

        end_time = time.time()
        elapsed_time = round((end_time - start_time),2)
        for i in result:
            data.append(i)
        # data += result
        print(f"{a} - {b} {elapsed_time}")
        with open(f'all_listing_urls.json', 'w') as f:
            json.dump(data, f)
        a += 100
        b += 100

        
        

        if a>1000:
            status = False
        # print(none_url)
        # time.sleep(2)