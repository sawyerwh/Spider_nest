# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from urllib.parse import quote
from jd.items import JdItem
from urllib.parse import urlencode

class DongziSpider(Spider):
    name = 'dongzi'
    allowed_domains = ['search.jd.com']
    start_urls = 'https://search.jd.com/Search?'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            data = {'keyword': keyword, 'enc': 'utf-8', 'wq': keyword}

            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                params = urlencode(data)
                url = self.start_urls + params
       
                print('*' * 20)
                print(url)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        products = response.xpath(
            '//div[@id="J_goodsList"]//li[@class="gl-item"]/div[contains(@class, "gl-i-wrap")]')
        
        print('-' * 20)
        print(len(products))

        for product in products:
            item = JdItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "p-price")]//i[1]/text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "p-name")]//text()').extract()).strip()
            # item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            # item['image'] = ''.join(product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            # item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            # item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item
