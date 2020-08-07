# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookClassItem(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()
    name = scrapy.Field()
    pcode = scrapy.Field()
    level = scrapy.Field()
    pass
