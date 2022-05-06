import scrapy
import pandas as pd
from scrapy import Item, Field
import re


class MovieItem(Item):
    title = Field()
    name = Field()
    url = Field()
    count = Field()  # 页数
    total = Field()  # 总数


class MoviesLinkSpider(scrapy.Spider):
    """
    获取所有视频网页链接
    """
    name = 'movies_link'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1.25,
        '': '',
        'DOWNLOADER_MIDDLEWARES': {
            'ddrk.middlewares.DdrkProxyUaDownloaderMiddleware': 543,
        },
        # 广度优先
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": 'scrapy.squeues.PickleFifoDiskQueue',
        "SCHEDULER_MEMORY_QUEUE": 'scrapy.squeues.FifoMemoryQueue',
        'FEEDS': {
            'datas/movies_link.csv': {
                'format': 'csv',
                'encoding': 'utf-8'
            }
        }
    }

    def start_requests(self):
        df = pd.read_csv('/home/*/Desktop/pyspider/ddrk/datas/movies_total.csv')
        df_length = len(df)
        for i in range(df_length):
            """
            count: page numbers code
            """
            series = df.iloc[i]
            format_url = series.iloc[0]
            count = series.iloc[1]
            title = series.iloc[2]
            total = series.iloc[3]
            for c in range(1, count + 1):
                s = f'/page/{c}/'
                url = format_url % s
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(title=title, cc=c, total=total))

    def parse(self, response, **kwargs):
        item = MovieItem()
        title = kwargs.get('title')
        movies = response.css('div.post-box-list>article')
        item['title'] = title
        count = kwargs.get('cc')
        total = kwargs.get('total')
        for movie in movies:
            item['count'] = count
            item['total'] = total
            item['name'] = movie.css('h2.post-box-title>a::text').get()
            item['url'] = movie.css('h2.post-box-title>a::attr(href)').get()
            yield item

