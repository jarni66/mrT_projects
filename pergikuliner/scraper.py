from function import *


def main():
    data = StoreItem()
    # regions = ['Jakarta', 'Bogor', 'Depok', 'Tangerang', 'Bekasi', 'Bandung', 'Surabaya']
    # regions = ['Jakarta Barat', 'Jakarta Pusat', 'Jakarta Selatan','Jakarta Timur','Jakarta Utara',
    #            'Bogor Barat', 'Bogor Timur', 'Bogor Utara', 'Bogor Selatan', 
    #            'Depok Timur', 'Depok II Tengah', 'Depok II Timur', 'Depok Town Center',
    #            'Tangerang City Mall', 'Tangerang Selatan', 'Kota Tangerang',
    #            'Bekasi Barat', 'Bekasi Timur', 'Bekasi Utara', 
    #            'Bandung Electronic Center', 'Bandung Indah Plaza', 'Bandung Trade Center', 'Hilton Bandung',
    #            'Surabaya Town Square','Bumi Surabaya City Resort','Plaza Surabaya','Sheraton Surabaya ']
    regions = get_district()
    files = get_outlist()
    for reg in regions:
        if reg not in files:
            for page in range(1,126):
                print(f"{reg} {page}")
                urls = get_url_head2(reg,page)
                if len(urls) != 0:
                    loop = asyncio.get_event_loop()
                    asyncio.set_event_loop(loop)
                    task = asyncio.ensure_future(run(urls,data))
                    loop.run_until_complete(task)
                    result = task.result().result()
                else:
                    print(f"PASS {reg} {page}")
                    break
                # if page%25 == 0:
                #     data.save_item(f'OUTPUT2/{reg}_{page}.json')
            data.save_item(f'OUTPUT3/{reg}.json')
            data.clear()
        else:
            pass