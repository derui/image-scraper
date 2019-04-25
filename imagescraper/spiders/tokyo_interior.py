# -*- coding: utf-8 -*-
import os
from imagescraper.items import ImageScraperItem
import scrapy

url_tag_map = {
    'https://www.tokyointerior-onlineshop.com/shopbrand/01/': 'sofa',
    'https://www.tokyointerior-onlineshop.com/shopbrand/01/page2/recommend/': 'sofa',
    'https://www.tokyointerior-onlineshop.com/shopbrand/01/page3/recommend/': 'sofa',
    'https://www.tokyointerior-onlineshop.com/shopbrand/02/': 'bed',
    'https://www.tokyointerior-onlineshop.com/shopbrand/02/page2/recommend/': 'bed',
    'https://www.tokyointerior-onlineshop.com/shopbrand/ct41/': 'table',
    'https://www.tokyointerior-onlineshop.com/shopbrand/ct42/': 'chair',
    'https://www.tokyointerior-onlineshop.com/shopbrand/ct60/': 'shelf',
    'https://www.tokyointerior-onlineshop.com/shopbrand/08/': 'bookshelf',
    'https://www.tokyointerior-onlineshop.com/shopbrand/08/page2/order/': 'bookshelf',
    'https://www.tokyointerior-onlineshop.com/shopbrand/10_1/': 'desk',
    'https://www.tokyointerior-onlineshop.com/shopbrand/10_2/': 'study_desk',
    'https://www.tokyointerior-onlineshop.com/shopbrand/ct279/': 'carpet',
    'https://www.tokyointerior-onlineshop.com/shopbrand/10_3/': 'desk_chair',
    'https://www.tokyointerior-onlineshop.com/shopbrand/ct105/': 'light'
}

class TokyoInteriorSpider(scrapy.Spider):
    name = "tokyo_interior"
    allowed_domains = ["www.tokyointerior-onlineshop.com"]

    def __init__(self, offset=None, *args, **kwargs):
        super(TokyoInteriorSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for item in url_tag_map.keys():
            print(item)

            yield self.make_requests_from_url(item)

    def parse(self, response):
        images = response.xpath('//ul[@class="innerList"]//div[@class="imgWrap"]//img')

        for image in images:
            file_url = image.xpath('@src').extract_first()

            if file_url is not None and not self.__should_ignore(file_url):

                item = ImageScraperItem(
                    tags=[url_tag_map[response.url]],
                    file_urls=[file_url],
                    files=[]
                )

                yield item

    def __should_ignore(self, url):
        p = os.path.basename(url)
        _, ext = os.path.splitext(p)

        ignoreable_exts = ['.gif']
        return ext in ignoreable_exts
