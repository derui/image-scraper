# -*- coding: utf-8 -*-
import os
from imagescraper.items import ImageScraperItem
import urllib
import scrapy

class TokyoInteriorSpider(scrapy.Spider):
    name = "otuka_kagu"
    allowed_domains = ["www.idc-otsuka.jp"]
    start_urls = [
        'https://www.idc-otsuka.jp/item/index.php?lcategory=sofa',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=bedframe',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=mattress',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=sfbed',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=dset&r1=1',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=dset&r1=3',
        'https://www.idc-otsuka.jp/item/index2.php?scategory=dchair',
    ]

    def __init__(self, offset=None, *args, **kwargs):
        super(TokyoInteriorSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        details = response.xpath('//div[contains(@class, "item_detail_list_area")]//a')

        for detail in details:
            detail_url = detail.xpath('@href').extract_first()
            detail_url = urllib.parse.urljoin(response.url, detail_url)

            category = urllib.parse.parse_qs(urllib.parse.urlparse(response.url).query)
            if 'lcategory' in category:
                category = category['lcategory'][0]
            elif 'scategory' in category:
                category = category['scategory'][0]
            yield scrapy.Request(detail_url,
                                 callback=self._parse_detail(category))

        pagings = response.xpath('//span[@class="nextprev" and contains(*, "次へ")]//a/@href').extract_first()

        if pagings is not None:
            page_url = pagings
            next_url = urllib.parse.urljoin(response.url, page_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def _parse_detail(self, category):
        def _parse(response):
            file_url = response.xpath('//img[contains(@class, "item_main")]/@src').extract_first()
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
