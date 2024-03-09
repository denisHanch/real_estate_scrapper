import scrapy
from parse_real_estate.items import ParseRealEstateItem   


class RealestatespiderSpider(scrapy.Spider):

    entries_num = 500
    per_page = 100
    pages = entries_num // per_page

    name = "realestatespider"
    allowed_domains = ["sreality.cz"]
    """
    API specifications:
        category_main_cb = 1    - Apartments for sale
        sort = 0                - New entriesfirst
        per_page                - Number of entries per page
        page                    - Page number
    """
    start_urls = [f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page={i}" \
                  for i in range(1,6)]

    def parse(self, response):

        #here we are looping through the products and extracting the name, price & url
        entries = response.json()['_embedded']['estates']

        item = ParseRealEstateItem()
        for entry in entries:

            item['name'] = entry['name']
            item['locality'] = entry['locality']
            item['price'] = entry['price']
            yield item
