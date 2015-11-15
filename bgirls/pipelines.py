# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class MongoDBPipeline(object):
    newItem = 0
    updatedItem = 0
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def open_spider(self,spider):
        print "begin"

    def close_spider(self,spider):
        print "%d newItem %d updated" % (self.newItem,self.updatedItem)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}".format(data))
        if valid:
            res = self.collection.replace_one({"_id" : item["_id"],},dict(item),True)
            if res.upserted_id:
                self.newItem += 1
                logging.log(logging.DEBUG,"a girl item insert")
            else:
                self.updatedItem += 1
        return item
