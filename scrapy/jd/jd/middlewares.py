# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import time
import random
from jd.settings import IPPOOL
from scrapy import signals
import time


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.timeout = timeout
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument("--proxy-server=%s" % request.meta["proxy"])

        self.browser = webdriver.Chrome(chrome_options = chromeOptions)            
        self.browser.set_window_size(1400, 700)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()
    
    def process_request(self, request, spider):
        """
        抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        page = request.meta.get('page', 1)
        try:
            # print(request.meta["proxy"])


            self.browser.get(request.url)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight / 8)')

            time.sleep(2)
            self.browser.execute_script('window.scrollTo(0, 2 * document.body.scrollHeight / 8)')
            time.sleep(2)

            self.browser.execute_script('window.scrollTo(0, 3 * document.body.scrollHeight / 8)')
            time.sleep(2)

            self.browser.execute_script('window.scrollTo(0, 4 * document.body.scrollHeight / 8)')
            time.sleep(2)

            self.browser.execute_script('window.scrollTo(0, 5 * document.body.scrollHeight / 8)')
            time.sleep(2)

            self.browser.execute_script('window.scrollTo(0, 6 * document.body.scrollHeight / 8)')
            time.sleep(2)

            self.browser.execute_script('window.scrollTo(0, 7 * document.body.scrollHeight / 8)')
            time.sleep(2)
            self.browser.execute_script('window.scrollTo(0, 8 * document.body.scrollHeight / 8)')

            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .input-txt')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn-default')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_topPage b'), str(page)))

 
            self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .input-txt')))
            # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
