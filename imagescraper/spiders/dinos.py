# -*- coding: utf-8 -*-
import os
from imagescraper.items import ImageScraperItem
import urllib
import scrapy

categories = {
    '002001020': 'sofa',
    '002001021': 'chair',
    '002001022': 'table',
    '002001023': 'chest',
    '002001019': 'wallstorage',
    '002001024001': 'rack',
    '002001024003': 'shelve',
    '002001025001': 'buffet',
    '002001025002': 'kitchencounter',
    '002001026001': 'chest',
    '002001026003': 'closet',
    '002001026002': 'wardrobe',
    '002001026004': 'closethanger',
    '002001026005': 'hangerrack',
    '002001026014': 'japanesechest',
    '002008001001': 'singlebed',
    '002008001003': 'doublebed',
    '002007002': 'carpet',
    '002007001': 'cartain',
    '002001032': 'kotatu',
}

def _match_category(url):
    v = list(map(lambda key: categories[key], filter(lambda key: url.find(key) != -1, categories)))

    if v == []:
        return "unknown"
    return v[0]

class DinosSpider(scrapy.Spider):
    name = "dinos"
    allowed_domains = ["www.dinos.co.jp"]
    start_urls = [
        'https://www.dinos.co.jp/c3/002001020/1a1/',
        'https://www.dinos.co.jp/c3/002001021/1a1/',
        'https://www.dinos.co.jp/c3/002001022/1a1/',
        'https://www.dinos.co.jp/c3/002001023/1a1/',
        'https://www.dinos.co.jp/c3/002001019/1a1/',
        'https://www.dinos.co.jp/c4/002001024001/1a2/',
        'https://www.dinos.co.jp/c4/002001024003/1a2/',
        'https://www.dinos.co.jp/c4/002001025001/1a2/',
        'https://www.dinos.co.jp/c4/002001025002/1a2/',
        'https://www.dinos.co.jp/c4/002001026001/1a2/',
        'https://www.dinos.co.jp/c4/002001026003/1a2/',
        'https://www.dinos.co.jp/c4/002001026002/1a2/',
        'https://www.dinos.co.jp/c4/002001026004/1a2/',
        'https://www.dinos.co.jp/c4/002001026005/1a2/',
        'https://www.dinos.co.jp/c4/002001026014/1a2/',
        'https://www.dinos.co.jp/c4/002008001001/1a2/',
        'https://www.dinos.co.jp/c4/002008001003/1a2/',
        'https://www.dinos.co.jp/c3/002007002/1a1/',
        'https://www.dinos.co.jp/c3/002007001/1a1/',
        'https://www.dinos.co.jp/c3/002001032/1a1/',
    ]

    def __init__(self, offset=None, *args, **kwargs):
        super(DinosSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        print(response.url)
        details = response.xpath('//div[@id="listPreview"]//div[@class="picPreview"]/a')

        for detail in details:
            detail_url = detail.xpath('@href').extract_first()
            detail_url = urllib.parse.urljoin(response.url, detail_url)

            category = _match_category(response.url)
            yield scrapy.Request(detail_url,
                                 callback=self._parse_detail(category))

        pagings = response.xpath('//li[@class="btn next"]/a/@href').extract_first()

        if pagings is not None:
            page_url = pagings
            next_url = urllib.parse.urljoin(response.url, page_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def _parse_detail(self, category):
        def _parse(response):
            file_url = response.xpath('//div[@class="first-image"]/img/@src').extract_first()
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
