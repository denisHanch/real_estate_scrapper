import scrapy
from parse_real_estate.items import ParseRealEstateItem   


class RealestatespiderSpider(scrapy.Spider):

    entries_num = 500
    per_page = 100
    pages = entries_num // per_page

    name = "realestatespider"
    allowed_domains = ["sreality.cz"]

    """
    API parameters:
        category_main_cb = 1    - Apartments for sale
        sort = 0                - New entriesfirst
        per_page                - Number of entries per page
        page                    - Page number
    """

    start_urls = [f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page={i}" \
                  for i in range(1,6)]

    def parse(self, response):

        #Get the list of apartments
        entries = response.json()['_embedded']['estates']

        item = ParseRealEstateItem()

        #Loop through the apartments and extract the needed data
        for entry in entries:

            #Replace non-break spaces with regular ones
            item['name'] = entry['name'].replace('\xa0', ' ')
            item['locality'] = entry['locality']
            item['price'] = entry['price']
            yield item
