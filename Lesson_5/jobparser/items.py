# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field()

    name = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    experience = scrapy.Field()
    condition = scrapy.Field()

    company_name = scrapy.Field()
    company_location = scrapy.Field()

