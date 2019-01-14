from selenium import webdriver
from proxy_pool_helper import get_proxy

# proxy = get_proxy()

proxy = '58.53.128.83:3128'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')
