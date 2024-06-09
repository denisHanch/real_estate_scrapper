import scrapy
from parse_real_estate.items import ParseRealEstateItem   


class RealestatespiderSpider(scrapy.Spider):

    # Total number of apartments to parse
    entries_num = 500

    # Search parameter for API
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

    start_urls = [f"https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page={i}" \
                  for i in range(1, 11)]

    def parse(self, response):

        #Get the list of apartments for the response object
        entries = response.json()['_embedded']['estates']

        item = ParseRealEstateItem()

        #Loop through the apartments and extract the needed data
        for entry in entries:

            #Replace non-break spaces with regular ones
            item['name'] = entry['name'].replace('\xa0', ' ')
            item['locality'] = entry['locality']
            item['price'] = entry['price']
            
            apt_props = entry['name'].replace('\xa0', ' ').split(" ")
            item['apt_type'] = apt_props[3]
            item['apt_size_m_sqrt'] = apt_props[4]

            adress = entry['locality'].replace('\xa0', ' ').split(",")
            item['street'] = adress[0]
            try:
                item['city'] = adress[1]
            except:
                item['city'] = adress[0]

            yield item
