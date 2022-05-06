import scrapy
import pandas as pd
from scrapy.item import Item, Field


class FileLinkItem(Item):
    name = Field()
    title = Field()
    total = Field()
    file_url = Field()


class VideoSpider(scrapy.Spider):
    """
    电影数据
    """
    name = 'video'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'RETRY_HTTP_CODES': [401, 403, 500, 502, 504, 504],
        'RETYR_TIMES': 5,
        'SPIDER_MIDDLEWARES': {
            'scrapy_deltafetch.DeltaFetch': 100,
        },
        'DELTAFETCH_ENABLED': True,
        'FEEDS': {
            'datas/VIDEO_LINKS.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
            }
        },
        # 'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'DOWNLOADER_MIDDLEWARES': {
            'ddrk.middlewares.DownloadMiddlewares': 543,
        },
        'ITEM_PIPELINES': {
            "ddrk.pipelines.SaveMongoPipeline": 300,
        }

    }
    df = pd.read_csv('/home/*/Desktop/pyspider/ddrk/datas/movies_link.csv')

    def start_requests(self):
        count = len(self.df)

        for cc in range(count):
            name = self.df.iloc[cc, 1]
            title = self.df.iloc[cc, 2]
            total = str(self.df.iloc[cc, 3])
            url = self.df.iloc[cc, 4]
            if not title.endswith('剧'):
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(name=name, title=title, total=total))

    def parse(self, response, **kwargs):
        item = FileLinkItem()
        item["name"] = kwargs.get('name')
        item["title"] = kwargs.get('title')
        item['total'] = kwargs.get('total')
        url = response.css('div#vjsp>video::attr(src)').get()
        item['file_url'] = url
        yield item


