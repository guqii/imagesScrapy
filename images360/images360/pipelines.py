# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#define mongo db pipline
import pymongo
class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
        
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
        
        
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
#define image download pipline 
class ImagePipline(ImagesPipeline):
    def get_media_requests(self,item,info):
        yield Request(item['url'])
   
    def item_completed(self,results,item,info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            return DropItem('image download failed  ')
        return item
        
    def file_path(self,request,response=None,info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name