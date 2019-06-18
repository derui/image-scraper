# -*- coding: utf-8 -*-
import os
from imagescraper.items import ImageScraperItem
import urllib
import scrapy
import json

url_tag_map = {
    'https://www.nitori-net.jp/store/ja/ec/BedFrameDrainboard?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedFrameStorage?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/LowBedFloorBed?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedFrameStandard?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedframePipeTatamiPipe?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedFoldingElectricFolding?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedFrameLegmattres?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedBunkLoft?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedBunkLoftLoft?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedframePipeTatamiTatami?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedFoldingElectricElectric?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/Sofabed?ptr=list': 'sofa,bed',
    'https://www.nitori-net.jp/store/ja/ec/BedDoubleCushion?ptr=list': 'bed',
    'https://www.nitori-net.jp/store/ja/ec/BedSideNightTable?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/ConsoleTable?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/MattressPocketcoil?ptr=list': 'mattress',
    'https://www.nitori-net.jp/store/ja/ec/MattressBonnellcoi?ptr=list':'mattress',
    'https://www.nitori-net.jp/store/ja/ec/MattressTeihanpatsu?ptr=list': 'mattress',
    'https://www.nitori-net.jp/store/ja/ec/MattressNoncoil?ptr=list': 'mattress',
    'https://www.nitori-net.jp/store/ja/ec/SofaCloth?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/SofaClothLeather?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/SofaLeather?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/SofaCompact?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/CouchCornerSofa?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/CornerSofa?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/LawtypeCornerSofa?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/RecliningSofa?ptr=list': 'sofa',
    'https://www.nitori-net.jp/store/ja/ec/PersonalSingleSofa?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/MassageSofa?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/ZaisuCoverChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/DiningTableSet?ptr=list': 'tableset',
    'https://www.nitori-net.jp/store/ja/ec/DiningTable?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/Counter?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/CenterTable?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/Zataku?ptr=list': 'zataku',
    'https://www.nitori-net.jp/store/ja/ec/KotatuTable?ptr=list': 'kotatutable',
    'https://www.nitori-net.jp/store/ja/ec/SimpleTableChairTable?ptr=list': 'table',
    'https://www.nitori-net.jp/store/ja/ec/Desk?ptr=list': 'desk',
    'https://www.nitori-net.jp/store/ja/ec/DiningChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/DiningChairBench?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/StoolFloordinin?ptr=list':'stool',
    'https://www.nitori-net.jp/store/ja/ec/CounterChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/SimpleTableChairChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/WorkChairStackingme?ptr=list':'chair',
    'https://www.nitori-net.jp/store/ja/ec/WorkChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/Cupboard?ptr=list': 'cupboard',
    'https://www.nitori-net.jp/store/ja/ec/ApplianceBoard?ptr=list': 'applianceboard',
    'https://www.nitori-net.jp/store/ja/ec/OvenBoard?ptr=list': 'ovenboard',
    'https://www.nitori-net.jp/store/ja/ec/KDKitchenStorageRenjirack?ptr=list': 'rack',
    'https://www.nitori-net.jp/store/ja/ec/KDKitchenStorageWagon?ptr=list': 'kitchenwagon',
    'https://www.nitori-net.jp/store/ja/ec/KDKitchenStorageUndercount?ptr=list':'kitchencount',
    'https://www.nitori-net.jp/store/ja/ec/TvStand?ptr=list': 'tvstand',
    'https://www.nitori-net.jp/store/ja/ec/CornerTVstand?ptr=list': 'tvstand',
    'https://www.nitori-net.jp/store/ja/ec/HighTypeTvStand?ptr=list': 'tvstand',
    'https://www.nitori-net.jp/store/ja/ec/LivingStorageSideboard?ptr=list': 'sideboard',
    'https://www.nitori-net.jp/store/ja/ec/LivingStorageCabinet?ptr=list': 'cabinet',
    'https://www.nitori-net.jp/store/ja/ec/LivingStorageDisplayrac?ptr=list': 'rack',
    'https://www.nitori-net.jp/store/ja/ec/LivingStorageCddvd?ptr=list': 'rack',
    'https://www.nitori-net.jp/store/ja/ec/RackShelfMetal?ptr=list': 'rack',
    'https://www.nitori-net.jp/store/ja/ec/RackShelfWood?ptr=list': 'rack',
    'https://www.nitori-net.jp/store/ja/ec/Chest?ptr=list': 'chest',
    'https://www.nitori-net.jp/store/ja/ec/WardrobeLocker?ptr=list': 'wardrobe',
    'https://www.nitori-net.jp/store/ja/ec/Dresser?ptr=list': 'dresser',
    'https://www.nitori-net.jp/store/ja/ec/ShoesBox?ptr=list': 'shoesbox',
    'https://www.nitori-net.jp/store/ja/ec/Bookshelf?ptr=list': 'bookshelf',
    'https://www.nitori-net.jp/store/ja/ec/StudyDesk?ptr=list': 'desk',
    'https://www.nitori-net.jp/store/ja/ec/StudyChair?ptr=list': 'chair',
    'https://www.nitori-net.jp/store/ja/ec/CeilingPendantLightCeiling?ptr=list': 'light',
    'https://www.nitori-net.jp/store/ja/ec/CeilingPendantLightPendant?ptr=list': 'light',
    'https://www.nitori-net.jp/store/ja/ec/ClipLight?ptr=list': 'light',
    'https://www.nitori-net.jp/store/ja/ec/FloorLamp?ptr=list': 'lamp',
    'https://www.nitori-net.jp/store/ja/ec/TableDeskLampTable?ptr=list': 'lamp',
}

class NitoriSpider(scrapy.Spider):
    name = "nitori"
    allowed_domains = ["www.nitori-net.jp"]

    def __init__(self, offset=None, *args, **kwargs):
        super(NitoriSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for item in url_tag_map.keys():
            print(item)

            yield self.make_requests_from_url(item)

    def parse(self, response):
        category = url_tag_map[response.url]
        links = response.xpath('//div[@class="productListingWidget"]//div[@class="image"]/a[@class="product-link"]')

        for link in links:
            detail_url = link.xpath('@href').extract_first()
            yield scrapy.Request(detail_url, callback=self._parse_detail(category))

    def _parse_detail(self, category):
        def _parse(response):
            json_content = response.xpath('//div[starts-with(@id, "entitledItem_")]/text()').extract_first()
            if json_content is not None:
                parsed = json.loads(json_content)
                file_url = parsed[0]["ItemImage"]

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
