import requests
from bs4 import BeautifulSoup
import re
from stores_data import stores

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"}

amazon_headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}

def get_exchange_rates():
    mnb_site = requests.get("https://www.mnb.hu/arfolyamok")
    soup = BeautifulSoup(mnb_site.content, 'html.parser')

    pattern = '([0-9]{1,})(,{1})([0-9]{2})'
    exchange_rates = {'EUR': None, 'USD': None, 'GBP': None}

    for key in exchange_rates.keys():
        for tr in soup.select('tr'):
            if key in tr.text:
                for td in tr:
                    if re.fullmatch(pattern, td.text):
                        exchange_rates[key] = td.text

    return exchange_rates

def create_urls(item):
    split_item = item.lower().split()
    result_urls = {"Alza": None, "Emag": None, "Amazon": None, "OnBuy": None}
    for key in stores.keys():
        store = stores[key]
        if key in result_urls.keys():
            result_urls[key] = store['base_url'] + store['search_params'] + store['separator'].join(split_item) + store['after_search_params']
        
    return(result_urls)

def get_alza_prices(url):
    alza_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(alza_response.content, 'html.parser')

    first_item = soup.find('div', class_='browsingitem')
    item_name = first_item.find('a', class_='browsinglink')["data-impression-name"]
    item_price = first_item.find('span', class_="c2").text.replace(u'\xa0', '')[:-2]
    alza_item = [item_name, item_price]
    print(alza_item)

def get_emag_prices(url):
    emag_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(emag_response.content, 'html.parser')

    first_item = soup.find('div', class_='card-item card-standard js-product-data')
    item_name = first_item.find('a', class_='card-v2-title').text
    item_price = first_item.find('p', class_="product-new-price").text.replace(u'.', '')[:-3]
    emag_item = [item_name, item_price]
    print(emag_item)

def get_amazon_prices(url):
    amazon_response = requests.get(url, headers=amazon_headers)
    soup = BeautifulSoup(amazon_response.content, 'html.parser')

    result_list = soup.find('div', class_="s-main-slot")
    first_item = result_list.find_all('div', class_="s-result-item")[1]
    item_name = first_item.find('span', class_='a-size-medium a-color-base a-text-normal').text
    item_name = (item_name[:75] + '...') if len(item_name) > 75 else item_name
    item_price = first_item.find('span', class_="a-offscreen").text[1:]
    item_price = round(375.05 * float(item_price), 0)
    amazon_item = [item_name, int(item_price)]
    print(amazon_item)

urls = create_urls('iphone 13 pro max 125gb')
get_alza_prices(urls['Alza'])
get_emag_prices(urls['Emag'])
get_amazon_prices(urls['Amazon'])