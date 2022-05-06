import scrapy
from scrapy import Item, Field



class FirsItem(Item):
    type_ = Field()
    link = Field()
    sub_type = Field()
    sub_link = Field()


class FirstLinkSpider(scrapy.Spider):
    """
    获取网站首页的视频分类名称以及对应的url链接地址
    """
    name = 'first_link'
    allowed_domains = ['ddrk.me']
    start_urls = ['https://ddrk.me/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOADER_DELAY': 0.25,
        'DOWNLOADER_MIDDLEWARES': {
            'ddrk.middlewares.DdrkProxyUaDownloaderMiddleware': 543,
        },
        'FEEDS': {
          'datas/ddrk_all_page.json': {
              'format': 'json',
              'indent': 4,
              'encoding': 'utf-8',
          }
        },
    }

    def parse(self, response):
        ul = response.css('ul#primary-menu>li')
        item = FirsItem()
        for li in ul:
            link = li.css('a::attr(href)').get()
            item["type_"] = li.css('a::text').get()
            item["link"] = link

            next_type = li.css('ul[role="menu"]>li')
            sub_type = list()
            sub_link = list()
            if next_type:
                for i in next_type:
                    sub_type.append(i.css('a::text').get())
                    sub_link.append(response.urljoin(i.css('a::attr(href)').get()))

            item["sub_type"] = sub_type if sub_type else None
            item["sub_link"] = sub_link if sub_link else None
            yield item
