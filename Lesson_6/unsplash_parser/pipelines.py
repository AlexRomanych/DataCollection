# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class UnsplashParserPipeline:
    def process_item(self, item, spider):
        return item


class UnsplashImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, spider):
        # print(item)
        if item['img_urls']:
            for img_url in item['img_urls']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['img_urls'] = [itm[1] for itm in results if itm[0]]
        return item


