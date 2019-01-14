# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem

class CatSpider(scrapy.Spider):
	name = 'cat'
	allowed_domains = ['maoyan.com']
	start_urls = ['http://maoyan.com/board/4']

	def start_requests(self):
		headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
			'Accept': 'application/json, text/plain, */*',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
			'Connection': 'keep-alive',
			'X-Requested-With': 'XMLHttpRequest',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}
		for i in range(10):
			yield scrapy.Request(url = 'http://maoyan.com/board/4?offset=%d' % (i * 10),
								headers = headers,
								method = 'GET',             
								callback = self.parse,
								)

	def parse(self, response):
		movie_names = response.xpath('//div[@class="movie-item-info"]//a/text()').extract()
		for movie_name in movie_names:
			maoyan_item = MaoyanItem()
			maoyan_item['name'] = movie_name
			yield maoyan_item			
