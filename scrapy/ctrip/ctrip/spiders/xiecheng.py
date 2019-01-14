# -*- coding: utf-8 -*-
import scrapy


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst']

    def parse(self, response):
        pass
