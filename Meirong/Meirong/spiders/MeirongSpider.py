# -*- coding: utf-8 -*-
import scrapy
from Meirong.items import MeirongItem

class MeirongpiderSpider(scrapy.Spider):
    name = "Meirong"
    allowed_domains = ["baixing.com"]
    start_urls = [
                  'http://xian.baixing.com/jiameng/m36461/'
                  ]

    def parse(self, response):
        list = response.css(".listing-ad")
        for one in list:
            item = MeirongItem()
            item['title'] = one.css(".ad-title::text").extract_first()
            item['phone'] = one.css(".contact-button::attr(data-contact)").extract_first()
            yield item
            next_url = response.css(".list-pagination li:last-child a::attr(href)").extract_first()
            next_text = response.css(".list-pagination li:last-child a::text").extract_first()
            print(next_text)
            if next_text == "下一页":
                # 下一页
                yield response.follow(next_url, callback=self.parse)