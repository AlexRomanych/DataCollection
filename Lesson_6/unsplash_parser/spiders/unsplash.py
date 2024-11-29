import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.unsplash_parser.items import UnsplashParserItem
from scrapy.loader import ItemLoader


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]

    def __init__(self, query=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):

        # Так как сайт написан на React.js, контент подгружается динамически
        # Поэтому скрейпим только текущую страницу
        links = response.xpath("//figure//a[@itemprop='contentUrl']/@href").getall()

        # Выбираем все картинки на странице
        categories = response.xpath("//figure")

        # В браузере xpath по этому запросу выдает 20 вхождений, scrapy выдает 60, из которых 40 повторяются
        # Выбираем уникальные
        index = 0
        correct_links = {}
        for link in links:
            tag = categories[index].xpath("./div")[0].xpath("./div")[1].xpath(".//a[@title]//text()").getall()
            correct_links[link] = tag
            index += 1

        for link, tags in correct_links.items():
            yield response.follow(link, callback=self.image_parse, meta={'tags': tags})

    def image_parse(self, response: HtmlResponse):
        tags = response.meta.get('tags')
        url = response.url
        name = response.xpath("//h1/text()").get()
        img_urls = response.xpath("//button//img[@srcset]/@srcset").get()

        # yield UnsplashParserItem(
        #     tags=tags, url=url, name=name, img_urls=img_urls
        # )

        loader = ItemLoader(item=UnsplashParserItem(), response=response)
        loader.add_value("tags", tags)
        loader.add_value("url", url)
        loader.add_value("name", name)
        loader.add_value("img_urls", img_urls)

        yield loader.load_item()
