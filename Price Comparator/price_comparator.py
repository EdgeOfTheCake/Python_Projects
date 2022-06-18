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
                        exchange_rates[key] = td.text.replace(",", ".")

    return exchange_rates

def create_urls(item):
    split_item = item.lower().split()
    result_urls = {"Alza": None, "Emag": None, "Amazon": None, "eBay": None}
    for key in stores.keys():
        store = stores[key]
        if key in result_urls.keys():
            result_urls[key] = store['base_url'] + store['search_params'] + store['separator'].join(split_item) + store['after_search_params']
        
    return(result_urls)

def get_alza_prices(url):
    alza_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(alza_response.content, 'html.parser')
    searched_item = "jabra elite active 75t"

    result_list = soup.find('div', class_="browsingitemcontainer")
    for item in result_list:
        if searched_item in item.text.lower():
            first_item = item
            break

    item_name = first_item.find('a', class_='browsinglink')["data-impression-name"]
    item_price = first_item.find('span', class_="c2").text[:-2].replace(u'\xa0', '')
    alza_item = [item_name, item_price]
    print(alza_item)

def get_emag_prices(url):
    emag_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(emag_response.content, 'html.parser')
    searched_item = "jabra elite active 75t"

    result_list = soup.find('div', class_="js-products-container")
    for item in result_list:
        if searched_item in item.text.lower():
            first_item = item
            break
    item_name = first_item.find('a', class_='card-v2-title').text
    item_price = first_item.find('p', class_="product-new-price").text[:-3].replace(u'.', '')
    emag_item = [item_name, item_price]
    print(emag_item)

def get_amazon_prices(url):
    amazon_response = requests.get(url, headers=amazon_headers)
    soup = BeautifulSoup(amazon_response.content, 'html.parser')
    searched_item = "jabra elite active 75t"

    result_list_outer = soup.find('div', class_="s-main-slot")
    result_list_inner = result_list_outer.find_all('div', class_="s-result-item")
    for item in result_list_inner:
        if "sponsored" in item.text.lower():
            continue
        if searched_item in item.text.lower():
            first_item = item
            break
    item_name = first_item.find('span', class_='a-size-medium a-color-base a-text-normal').text
    item_name = (item_name[:75] + '...') if len(item_name) > 75 else item_name
    item_price = first_item.find('span', class_="a-offscreen").text[1:].replace(",", "")
    item_price = round(375.05 * float(item_price), 0)
    amazon_item = [item_name, int(item_price)]
    print(amazon_item)


def get_ebay_prices(url):
    ebay_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(ebay_response.content, 'html.parser')
    searched_item = "jabra elite active 75t"

    result_list = soup.find('ul', class_="srp-results srp-list clearfix")
    for item in result_list:
        if searched_item in item.text.lower():
            first_item = item
            break
    item_name = first_item.find('h3', class_='s-item__title').text
    item_name = (item_name[:50] + '...') if len(item_name) > 50 else item_name
    item_price = first_item.find('span', class_="s-item__price").text[1:].replace(",", "")
    item_price = price_converter(item_price, "USD", True)
    ebay_item = [item_name, item_price]
    print(ebay_item)

def price_converter(price, currency, to_huf=True):
    currency_exchange_rate = float(get_exchange_rates()[currency])
    if to_huf:
        item_price = round(currency_exchange_rate * float(price), 0)
        return int(item_price)
    else:
        item_price = round(float(price) / currency_exchange_rate, 2)
        return item_price

urls = create_urls('jabra elite active 75t')
get_alza_prices(urls['Alza'])
get_emag_prices(urls['Emag'])
get_amazon_prices(urls['Amazon'])
get_ebay_prices(urls['eBay'])