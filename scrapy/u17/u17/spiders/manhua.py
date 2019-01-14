# -*- coding: utf-8 -*-
import scrapy
import json
from u17.agent_helper import get_random_agent
from u17.items import U17Item


class ManhuaSpider(scrapy.Spider):
    name = 'manhua'
    allowed_domains = ['www.u17.com']
    start_urls = ['http://www.u17.com/']

    def start_requests(self):
        data = { 'data[group_id]': 'no', 'data[theme_id]': 'no', 'data[is_vip]': 'no', 'data[accredit]': 'no', 'data[color]': 'no', 'data[comic_type]': 'no', 'data[series_status]': 'no', 'data[order]': '2', 'data[page_num]': '2', 'data[read_mode]': 'no' }
        base_url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'

        for page in range(411):
            agent = get_random_agent()
            headers = {
                'Referer': base_url,
                'User-Agent': agent,
                'Host': 'www.u17.com',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            data['data[page_num]'] = str(page + 1)

            yield scrapy.FormRequest(url = base_url,
                         headers = headers,
                         method = 'POST',
                         formdata = data,
                         callback = self.parse,
                         )

    def parse(self, response):
        json_result = json.loads(response.text)
        comic_list = json_result['comic_list']
        for comic in comic_list:
            item = U17Item()
            item['comic_id'] = comic.get('comic_id', '')
            item['title'] = comic.get('name', '')
            item['classify'] = comic.get('line2', '')
            item['cover'] = comic.get('cover', '')

            yield item

