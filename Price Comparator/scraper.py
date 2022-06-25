import requests
from bs4 import BeautifulSoup
import re

from currency_parser import price_converter



class Scraper:

    def __init__(self, endpoint_data, searched_item):
        self.endpoint_data = endpoint_data
        self.searched_item = searched_item
        self.scrape_results = []

    def get_exchange_rates(self):
        response = requests.get(self.endpoint_data.currency_rates["url"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            pattern = '([0-9]{1,})(,{1})([0-9]{2})'

            for currency in self.endpoint_data.currency_rates["currencies"]:
                for tr in soup.select('tr'):
                    if currency["name"] in tr.text:
                        for td in tr:
                            if re.fullmatch(pattern, td.text):
                                currency["rate"] = td.text.replace(",", ".")
        else:
            raise Exception(f"Could not connect to {self.endpoint_data.currency_rates['url']}")
        

    def create_urls(self):
        split_item = self.searched_item.lower().split()
        try:
            for endpoint in self.endpoint_data.endpoint_data["endpoints"]:
                endpoint['result_url'] = endpoint['base_url'] + endpoint['before_item_search'] + endpoint['separator'].join(split_item) + endpoint['after_item_search']
        except KeyError:
            print(f"Creating url Failed at {endpoint['name']}: Wrong key!\n")

    def set_up_data(self):
        self.get_exchange_rates()
        self.create_urls()

        print("Setting up endpoint data and currencies done.")

    def scrape_endpoints(self):
        self.set_up_data()
        for endpoint in self.endpoint_data.endpoint_data["endpoints"]:
            try:
                self.scrape_endpoint(endpoint)
            except Exception:
                print(f"Could not establish a connection to {endpoint['name']}'s site. Scraper will jump to next endpoint.")


    def scrape_endpoint(self, endpoint):
        response = requests.get(endpoint['result_url'], headers=endpoint['headers'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            endpoint_info = endpoint["scrape_info"]

            try:
                result_list = soup.find(endpoint_info["result_list_tag"], class_=endpoint_info["result_list_class"])
                if endpoint_info["need_inner_find"]:
                    result_list = result_list.find_all(endpoint_info["inner_result_list_tag"], class_=endpoint_info["inner_result_list_class"])

                for item in result_list:
                    if self.searched_item in item.text.lower():
                        first_item = item
                        break

                item_name, item_price = self.get_name_and_price(first_item, endpoint_info)
                self.scrape_results.append({"Shop": endpoint['name'], "Product": item_name, "Price": item_price})

            except AttributeError:
                print(f"Could not find valid field to scrape on {endpoint['result_url']}\nSome field is wrong in endpoint['scrape_info']: {endpoint_info}")
            except KeyError as key_err:
                print(f"{key_err} is missing form scrape info at {endpoint['name']}")
            except Exception as e:
                print(e)

        else:
            print(f"{response.status_code}, Could not reach site {endpoint['base_url']}")

    def get_name_and_price(self, item, endpoint):
        item_name = item.find(endpoint["item_name_tag"], class_=endpoint["item_name_class"]).text
        item_name = (item_name[:50] + '...') if len(item_name) > 50 else item_name

        item_price = item.find(endpoint["item_price_tag"], class_=endpoint["item_price_class"])
        item_price = item_price.text if endpoint["item_price_inner_tag"] == "" else item_price.find(endpoint["item_price_inner_tag"]).text
        
        for key, value in endpoint["replace"].items():
            item_price = item_price.replace(key, value)
        item_price = "".join(item_price.split())

        if endpoint["change_price_from_huf"]:
            item_price = price_converter(item_price, self.endpoint_data.currency_rates['currencies'], "USD", True)

        return item_name, item_price

