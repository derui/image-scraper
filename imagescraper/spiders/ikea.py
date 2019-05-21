# -*- coding: utf-8 -*-
import os
from imagescraper.items import ImageScraperItem
import urllib
import scrapy

urls = {
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/20489/': 'mirror',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10663/': 'sofa-bed',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10661/': 'sofa',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10687/': 'armchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10696/': 'armchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/35184/': 'armchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/35186/': 'armchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/20907/': 'armchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/20926/': 'ottoman',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10662/': 'sofa',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/16238/':'sofa',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10382/': 'bookstand',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10475/': 'dashboard',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/11465/': 'shelf',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10705/': 'sidetable',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10412/': 'sideboard',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/16246/': 'consoletable',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10409/': 'cabinet',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/10410/': 'collectioncase',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/20660/': 'wallshelf',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/20658/': 'shelf',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/living_room/20659/': 'bracket',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/10451/': 'chest',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/36209/': 'diningset',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/36212/': 'diningset',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/36213/': 'diningset',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/lighting/10732/': 'tablelamp',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/lighting/10731/': 'floorlamp',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/lighting/20502/': 'worklamp',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/25219/': 'chair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/workspaces/20652/': 'chair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/21825/': 'diningtable',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/25219/': 'diningchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/dining_storage/': 'diningstorage',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/20862/': 'bartable',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/20864/': 'barchair',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/19145/': 'diningset',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/20656/': 'bedside',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/dining/10728/': 'stool',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/workspaces/20649/': 'desk',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/19039/': 'loftbed',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/16285/': 'singlebed',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/16284/': 'doublebed',
    'https://www.ikea.com/jp/ja/catalog/categories/departments/bedroom/25205/': 'bed',
}

class IKEASpider(scrapy.Spider):
    name = "ikea"
    allowed_domains = ["www.ikea.com"]
    start_urls = urls.keys()

    def __init__(self, offset=None, *args, **kwargs):
        super(IKEASpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        details = response.xpath('//a[@class="productLink"]')

        for detail in details:
            detail_url = detail.xpath('@href').extract_first()
            detail_url = urllib.parse.urljoin(response.url, detail_url)

            category = urls[response.url]
            yield scrapy.Request(detail_url,
                                 callback=self._parse_detail(category))

    def _parse_detail(self, category):
        def _parse(response):
            file_url = response.xpath('//img[@id="productImg"]/@src').extract_first()
            if file_url is not None and not self.__should_ignore(file_url):

                item = ImageScraperItem(
                    tags=[category],
                    file_urls=[urllib.parse.urljoin(response.url, file_url)],
                    files=[]
                )

                yield item

        return _parse

    def __should_ignore(self, url):
        p = os.path.basename(url)
        _, ext = os.path.splitext(p)

        ignoreable_exts = ['.gif']
        return ext in ignoreable_exts
