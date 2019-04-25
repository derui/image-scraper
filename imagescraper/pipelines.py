# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline, FileException
import cv2


class ImageScraperPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(ImageScraperPipeline, self).__init__(store_uri, download_func,
                                                   settings)

    # def get_media_requests(self, item, info):
    #     headers = item['response'].headers.copy()
    #     headers['referer'] = item['response'].url
    #     return [scrapy.Request(item.get('file_urls')[0], headers=headers)]

    def item_completed(self, results, item, info):

        ok, x = results[0]
        if not ok:
            raise FileException("Item not contains")

        item['files'] = [x['path']]
        tags = item['tags']
        item['tags'] = {}

        self._save_tags(x['path'], tags)
        self._constraint_image(x['path'])

        return item

    def _save_tags(self, path, tags):
        basedir = os.path.join(self.store.basedir, 'tags')
        filename, _ = os.path.splitext(os.path.basename(path))

        if not os.path.exists(basedir):
            os.makedirs(basedir)

        tagfile = os.path.join(basedir, filename + '.tsv')

        with open(tagfile, "w") as f:
            f.write("\t".join(tags) + "\n")

    def _constraint_image(self, path):

        try:
            img = cv2.imread(os.path.join(self.store.basedir, path))

            if img is None:
                raise DropItem('Item is not readable')

            cv2.imwrite(os.path.join(self.store.basedir, path), img)

        except DropItem:
            pass
