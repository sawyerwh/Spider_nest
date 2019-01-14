#!/usr/bin/python3
# coding=utf-8
import requests
from lxml import etree
import pymysql


# 获取页面HTML
def get_one_page(url):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
    try:
        response = requests.get(url, headers=headers)
    except:
        print('请求已中断，请尝试重新连接...')
        return None
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


# 第一层 解析
def parse_name(html):
    etree_html = etree.HTML(html)
    first_name = etree_html.xpath('//a[@class="btn btn2"]/text()')
    name_link = etree_html.xpath('//a[@class="btn btn2"]/@href')
    # 返回姓氏列表 和 姓氏链接列表
    return first_name, name_link


# 第二层 解析
def parse_name_detail(html):
    etree_html = etree.HTML(html)
    name_list = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
    name_list_link = etree_html.xpath('//div[@class="col-xs-12"]/a/@href')
    # 返回 姓名列表 和 姓名链接列表
    return name_list, name_list_link


# 第三层 解析
def parse_name_means(html):
    etree_html = etree.HTML(html)
    name_means = etree_html.xpath('//div[@class="panel panel-info"]/div[@class="panel-body"]/strong/text()')
    # 返回 名字总解 列表
    return name_means


# 保存数据库
def save_data(one_first_names):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'name_all'
    port = 3306
    db = pymysql.connect(host, user, password, database, port)
    cursor = db.cursor()
    for item in one_first_names:
        data1 = (item['first_name'], item['name'], item['means'])
        sql = "insert into names(first_name,name,means) values ('%s','%s','%s')" % data1
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()
    print('保存一个姓氏')


def main():
    # 第一层
    url = "http://www.resgain.net/xmdq.html"
    # 第一层页面获取 html
    html = get_one_page(url)
    # 第一层页面解析 获取 姓氏分类 及 姓氏链接
    first_name_result = parse_name(html)
    # print(first_name_result[0])

    # 第二层
    for i in range(len(first_name_result[1])):
        # 获取当前 姓氏名称  后期存字典
        first_name = first_name_result[0][i]
        # 获取当前 姓氏url（不完整）
        item = first_name_result[1][i]
        # 第二层 姓氏url 补全
        url01 = 'http:' + item
        url02 = url01.split('.html', 1)[0]

        # 第二层 分页 共 10页
        one_first_names = []
        for j in range(1, 11):
            url = url02 + '_%s.html' % j
            # 第二层 页面获取 html
            html01 = get_one_page(url)
            # 第二层 页面解析 获取 姓名 及 第三层链接
            result = parse_name_detail(html01)
            # print(result[0])

            # 第三层
            one_page_names = []
            for a in range(len(result[1])):
                # 获取 当前姓名 后期存字典
                name = result[0][a]
                # 获取 当前姓名url(不完整)
                item1 = result[1][a]
                # 第三层 姓名url 补全
                url03 = url.split('/name_list', 1)[0]
                url04 = url03 + item1
                # 第三层 页面获取 html
                # print(url04)
                html_detail = get_one_page(url04)
                # 第三层 页面解析 获取名字总解
                means = parse_name_means(html_detail)

                one_name = {}
                one_name['first_name'] = first_name
                one_name['name'] = name
                if len(means):
                    one_name['means'] = means[0]
                else:
                    one_name['means'] = None
                print(a)
                one_page_names.append(one_name)

            print('爬取一个分页')
            one_page_names.extend(one_page_names)

        print('爬取一个姓氏')
        save_data(one_first_names)

    print('完成')


if __name__ == '__main__':
    main()