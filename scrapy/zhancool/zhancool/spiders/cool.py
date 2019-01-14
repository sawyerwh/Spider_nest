# -*- coding: utf-8 -*-
import scrapy
import json
from zhancool.items import ZhancoolItem
from zhancool.agent_helper import get_random_agent

class CoolSpider(scrapy.Spider):
    name = 'cool'
    allowed_domains = ['hellorf.com']
    start_urls = ['http://www.hellorf.com/']

    # custom_settings = { 'DOWNLOAD_DELAY': 1, 'CONCURRENT_REQUESTS_PER_IP': 4 }

    def start_requests(self):
        headers = {
            'Referer': 'https://www.hellorf.com/image/search?q=%E7%BD%91%E7%AB%99',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'api.hellorf.com'
        }

        for i in range(10):
            data = {'keyword': '网站', 'page': '%d' % (i + 1)}
            headers['User-Agent'] = get_random_agent()
            print(headers['User-Agent'])

            yield scrapy.FormRequest(url = 'https://api.hellorf.com/hellorf/image/search?page=%d' % (i + 1),
                                headers = headers,
                                formdata = data,
                                method = 'POST',
                                callback = self.parse,
                                )

    def parse(self, response):
        json_result = json.loads(response.text)
        data_list = json_result['data']['data']
        for data in data_list:
            item = ZhancoolItem()
            item['item_id'] = data.get('_id', '')
            item['title'] = data.get('title', '')
            item['preview_url'] = data.get('preview_url', '')
            yield item
