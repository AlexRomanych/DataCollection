# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose, Identity


def parse_urls(urls):

    output = []
    values = urls[0].split(',')

    for value in values:
        details = value.strip().split(' ')
        output.append(details[0])

    return output


class UnsplashParserItem(scrapy.Item):

    tags = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    img_urls = scrapy.Field(output_processor=Compose(parse_urls))
