# -*- coding: utf-8 -*-
import scrapy
from loldesk.items import LoldeskItem


class loldeskpiderSpider(scrapy.Spider):
    name = "loldesk"
    allowed_domains = ["www.win4000.com"]
    # 抓取链接
    start_urls = [
        'http://www.win4000.com/zt/lol.html'
    ]

    def parse(self, response):
        list = response.css(".Left_bar ul li")
        for img in list:
            imgurl = img.css("a::attr(href)").extract_first()
            imgurl2 = str(imgurl)
            next_url = response.css(".next::attr(href)").extract_first()
            if next_url is not None:
                # 下一页
                yield response.follow(next_url, callback=self.parse)

            yield scrapy.Request(imgurl2, callback=self.content)

    def content(self, response):
        item = LoldeskItem()
        item['name'] = response.css(".pic-large::attr(title)").extract_first()
        item['ImgUrl'] = response.css(".pic-large::attr(src)").extract()
        yield item
        # 判断页码
        next_url = response.css(".pic-next-img a::attr(href)").extract_first()
        allnum = response.css(".ptitle em::text").extract_first()
        thisnum = next_url[-6:-5]
        if int(allnum) > int(thisnum):
            # 下一页
            yield response.follow(next_url, callback=self.content)
