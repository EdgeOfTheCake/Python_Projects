from endpoint_data import EndpointData
from scraper import Scraper
from visualizer import Visualizer

if __name__ == "__main__":
    endpoint_data = EndpointData()
    endpoint_data.read_data(["data/endpoint_data.json", "data/currency_exchange_data.json"])

    searched_item = "iphone 13"
    scraper = Scraper(endpoint_data, searched_item)
    scraper.scrape_endpoints()

    visualize = Visualizer(scraper.scrape_results)
    visualize.visualize_products()