import json


def pageurl(x,page,agent_id):
    if x == 'resident_sell':
        return f'https://www.rumah.com/properti-dijual/{page}?agent_id={agent_id}&market=residential'
    elif x == 'resident_rent':
        return f'https://www.rumah.com/properti-disewa/{page}?agent_id={agent_id}&market=residential'
    elif x == 'commercial_sell':
        return f'https://www.rumah.com/properti-dijual/{page}?agent_id={agent_id}&market=commercial'
    else:
        return f'https://www.rumah.com/properti-disewa/{page}?agent_id={agent_id}&market=commercial'



def scrape_item(soup_prop, prop):
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
        agent_phone = soup_prop.find('a',{'class':'actionable-link btn-outline-secondary btn'}).get('href').split('=')[1].split('&')[0]
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
    data['phone'] = agent_phone


    return data


def prop_page(link):
    
                    
    try:
        # print(f"n_AGENT {agent_ids.index(agent_id)}, SCRAPE {scrape} {link.split('/')[-1]}")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})
        driver.get(url=link)
        soup_prop = BeautifulSoup(driver.page_source, 'html.parser')

        data = scrape_item(soup_prop=soup_prop, prop=link)
        
        datas.append(data)

        with open('agent_prop.json', 'w') as f:
            json.dump(datas, f)
    except:
        pass