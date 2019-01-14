#!/usr/bin/python3
# coding=utf-8
from bs4 import BeautifulSoup
import requests


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_soup(html):
    soup = BeautifulSoup(html, 'lxml')                      # 试⽤用lxml解析器器构造beautifulsoup
    # print(soup.prettify())                                # 取⽹网⻚页缩进格式化输出
    # print(soup.title.string)                              # 取⽹网⻚页title内容
    # print(soup.head)                                      # 取⽹网⻚页head内容
    # print(soup.p)                                         # 取⽹网⻚页p标签内容
    # print(soup.title.name)                                # 获取节点的名字
    # print(soup.img.attrs["src"])                          # 获取节点属性
    # print(soup.p.contents)                                # 取p节点下⾯面所有⼦子节点列列表
    # print(soup.p.descendants)                             # 取p节点所有⼦子孙节点
    # print(soup.a.parent)                                  # 取⽗父节点
    # print(soup.a.parents)                                 # 取所有祖先节点
    # print(soup.a.next_sibling)                            # 同级下⼀一节点
    # print(soup.a.previous_sibling)                        # 同级上⼀一节点
    # print(soup.a.next_siblings)                           # 同级所有后⾯面节点
    # print(soup.a.previous_siblings)                       # 同级所有前⾯面节点
    # print(list(soup.a.parents)[0].attrs['class'])
    print(soup.p.sring)


def main():
    num = 1
    for j in range(4):
        page = ''
        if num >= 2:
            page = '_' + str(num)
        num += 1
        url = "http://moe.005.tv/73855%s.html" % str(page)
        html = get_one_page(url)
        result = parse_soup(html)
        # parse_with_xpath(html)


if __name__ == '__main__':
    main()
