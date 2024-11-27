import scrapy
from scrapy.http import HtmlResponse
from Lesson_5.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=Fullstack&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        # //span[@data-qa='vacancy-experience']//text() - Опыт работы
        # //p[@data-qa='vacancy-view-employment-mode']//text() - Вид работы
        # //div[@data-qa='vacancy-company__details']//text() - Компания название
        # //div[@class='vacancy-company-redesigned']//span[@data-qa='vacancy-view-link-location-text']//text() - Город
        # //div[@data-qa='vacancy-description']//text() - Описание вакансии

        url = response.url
        _id = int(url.split("/")[-1].split("?")[0])

        name = response.xpath("//h1[@data-qa='vacancy-title']//text()").getall()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        description = response.xpath("///div[@data-qa='vacancy-description']//text()").getall()
        experience = response.xpath("//span[@data-qa='vacancy-experience']//text()").get()
        condition = response.xpath("//p[@data-qa='vacancy-view-employment-mode']//text()").getall()
        company_name = response.xpath("//div[@data-qa='vacancy-company__details']//text()").getall()
        company_location = response.xpath("//div[@class='vacancy-company-redesigned']//span[@data-qa='vacancy-view-link-location-text']//text()").getall()

        yield JobparserItem(
            _id=_id,
            name=name,
            salary=salary,
            condition=condition,
            description=description,
            url=url,
            experience=experience,
            company_name=company_name,
            company_location=company_location,
        )



