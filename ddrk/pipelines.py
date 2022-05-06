# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class DdrkPipeline:
    def process_item(self, item, spider):
        return item


class SaveMongoPipeline:
    def open_spider(self, spider):
        host = spider.settings.get('MONGO_URL', 'localhost')
        port = spider.settings.get('MONGO_PORT', 27017)
        db = spider.settings.get('MONGO_DATABASE', 'ddrk')
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db]
        self.collection = self.db['video_info']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
