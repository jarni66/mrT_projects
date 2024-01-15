from function import *

# datas = []
# category = getCat()

# for cat in category:
#     cat_name = cat.split('/')[-2:]
#     resto_urls = getCatNav(cat)

#     for resto_url in resto_urls:
#         try:
#             print(f"{cat_name} {category.index(cat)}/{len(category)-1}, {resto_urls.index(resto_url)} / {len(resto_urls)-1}")
            
#             data = getRestoDetails(resto_url)
#             datas.append(data)
#         except:
#             print(f"FAIL {cat_name} {category.index(cat)}/{len(category)-1}, {resto_urls.index(resto_url)} / {len(resto_urls)-1}")
    
#     with open(f'OUTPUT/data_{category.index(cat)}of{len(category)-1}.json', 'w') as f:
#         json.dump(datas, f)

def main2():
    datas = []
    category = getCat()

    for cat in category[16:]:
        cat_name = cat.split('/')[-2:]
        resto_urls = getCatNav(cat)

        stats = True
        sec = 0
        while sec < len(resto_urls):
            try:
                url_list = resto_urls[sec:sec+10]
                data = scrape_urls(url_list)
                datas += data
                print(f"{cat_name} {category.index(cat)}/{len(category)-1}, {sec}/{len(resto_urls)}")
                sec += 10
            except:
                print(f"FAIL {cat_name} {category.index(cat)}/{len(category)-1}, {sec}/{len(resto_urls)}")
                sec += 10
                

        with open(f'OUTPUT/data_{category.index(cat)}of{len(category)-1}.json', 'w') as f:
            json.dump(datas, f)

def main_nonResto():
    datas = []
    category = getNonResto()

    for cat in category[14:]:
        cat_name = cat.split('/')[-2:]
        try:
            resto_urls = getCatNav(cat)
        except:
            continue

        stats = True
        sec = 0
        while sec < len(resto_urls):
            try:
                url_list = resto_urls[sec:sec+10]
                data = scrape_urls(url_list)
                datas += data
                print(f"{cat_name} {category.index(cat)}/{len(category)-1}, {sec}/{len(resto_urls)}")
                sec += 10
            except:
                print(f"FAIL {cat_name} {category.index(cat)}/{len(category)-1}, {sec}/{len(resto_urls)}")
                sec += 10
                

        with open(f'OUTPUT/non_resto/data_{category.index(cat)}of{len(category)-1}.json', 'w') as f:
            json.dump(datas, f)
            
main_nonResto()