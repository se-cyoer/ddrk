import scrapy
import json
from scrapy import Item, Field
import re


class MiItem(Item):
    title = Field()
    page_count = Field()
    total = Field()
    format_url = Field()


class MoviesInfoSpider(scrapy.Spider):
    """
    获取所有影视类型的相关信息（包括页面总数，影视名称、类型、总数）
    """
    name = 'movies_info'
    # allowed_domains = ['ddrk.me']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOADER_MIDDLEWARES': {
            'ddrk.middlewares.DdrkProxyUaDownloaderMiddleware': 543,
        },
        # 广度优先
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": 'scrapy.squeues.PickleFifoDiskQueue',
        "SCHEDULER_MEMORY_QUEUE": 'scrapy.squeues.FifoMemoryQueue',
        'FEEDS': {
            'datas/movies_total.csv': {
                'format': 'csv',
                'encoding': 'utf-8'
            }
        }
    }

    def start_requests(self):
        items = json.load(open('/home/*/Desktop/pyspider/ddrk/datas/ddrk_all_page.json'))
        for item in items:
            link = item.get('link')
            urls = item.get('sub_link')
            if link.startswith('http'):
                yield scrapy.Request(url=link, callback=self.parse)
            if urls:
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # 两个逻辑判断能保证数据经过刷选后总量是一样的
        item = MiItem()
        title = re.sub('(低端影视)|( 归档 - )', '', response.xpath('//title/text()').get())
        count = response.xpath('//div[@class="nav-links"]/a[@class="page-numbers"][2]/text()').get()
        movie_count = len(response.css('div.post-box-list>article'))
        end_page_url = response.xpath('//div[@class="nav-links"]/a[@class="page-numbers"][2]/@href').get()
        if count:
            count = int(count)
            total = (int(count) - 1) * movie_count
            item['title'] = title
            item['page_count'] = count
            item['total'] = total
            item['format_url'] = re.sub('/page/\d+/', '%s', end_page_url)
        if end_page_url:
            yield scrapy.Request(url=end_page_url, callback=self.detail_parse, cb_kwargs=dict(item=item))

    def detail_parse(self, response, item):
        item = item
        movies_count = len(response.css('div.post-box-list>article'))
        item['total'] = item['total'] + movies_count
        yield item
