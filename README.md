### ddrk.me 站点抓取视频信息以及视频链接

+ datas **数据存储**,ddrk **项目文件夹** 

  1. ddrk_all_page => first_link.py (获取网站首页的视频分类名称以及对应的url链接地址)
  2.  movies_total => movies_info.py (获取所有影视类型的相关信息（包括页面总数，影视名称、类型、总数）)
  3. movies_link => movies_link.py (获取所有视频网页链接)
  4. VIDEO_LINKS => VIDEO_LINKS.csv (获取所有视频下载链接)

+ 视频相关信息存储在本地磁盘以及远程数据库（但只爬取了电影的数据）
  + 本地存储custom_settings中通过feeds中指定
  + 数据库存储，pipelines中指定
+ 电视剧修改video.py和middlewares
  + video.py
    + ````python
          def start_requests(self):
          count = len(self.df)
          for cc in range(count):
              name = self.df.iloc[cc, 1]
              title = self.df.iloc[cc, 2]
              total = str(self.df.iloc[cc, 3])
              url = self.df.iloc[cc, 4]
              if title.endswith('剧'):
                  yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(name=name, title=title, total=total))
+ 修改粗存地址和读取数据地址
  + ····shell
  /home/*/Desktop/pyspider/ddrk/datas 
  将*改为对应的
