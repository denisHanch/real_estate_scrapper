# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParseRealEstateItem(scrapy.Item):
    # Fields definition
    name = scrapy.Field()
    locality = scrapy.Field()
    price = scrapy.Field()
