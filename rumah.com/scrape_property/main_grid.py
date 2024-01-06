
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium import webdriver
# from seleniumwire import webdriver
import time
from bs4 import BeautifulSoup
import json
from prop_func import *
import concurrent.futures
from selenium.webdriver import DesiredCapabilities
import tqdm

with open('miss_phone.json') as f:
    out = json.load(f)

urls = out['link']


datas = []
def get_soup(url):
    ua = UserAgent(browsers=['chrome'])
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--no-sandbox")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('--log-level=3')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--user-agent={ua.random}")
    # chrome_options.add_extension('Privacy-Pass.crx')
    # chrome_options.set_capability("browserVersion", "67")
    # chrome_options.set_capability("platformName", "Windows XP")

    driver = webdriver.Remote(command_executor='http://localhost:4444',
                              options=chrome_options)
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = scrape_item(soup_prop=soup, prop=url)
    datas.append(data)
    with open('property_miss_phone.json', 'w') as f:
        json.dump(datas, f)
    driver.quit()
    print(f'DONE {urls.index(url)} of {len(urls)}')
    # driver.exit()
    # return data




with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(get_soup,urls))

        


