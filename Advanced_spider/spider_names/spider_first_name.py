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
    first_names_list = []
    etree_html = etree.HTML(html)
    first_name = etree_html.xpath('//a[@class="btn btn2"]/text()')
    name_link = etree_html.xpath('//a[@class="btn btn2"]/@href')
    for i in range(len(first_name)):
        first_names_dic = {}
        first_names_dic['first_names'] = first_name[i]
        first_names_dic['first_names_link'] = name_link[i]
        first_names_list.append(first_names_dic)
    # 返回姓氏列表 和 姓氏链接列表
    return first_names_list


# 保存数据库
def save_data(first_names_list):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'name_all'
    port = 3306
    db = pymysql.connect(host, user, password, database, port)
    cursor = db.cursor()
    for item in first_names_list:
        print(item)
        data1 = (item['first_names'], item['first_names_link'])
        sql = "insert into first_names(first_names, first_names_link) values ('%s','%s')" % data1
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()
    print('successful')


def main():
    # 第一层
    url = "http://www.resgain.net/xmdq.html"
    # 第一层页面获取 html
    html = get_one_page(url)
    # 第一层页面解析 获取 姓氏分类 及 姓氏链接
    first_names_list = parse_name(html)
    # print(first_names_list)

    save_data(first_names_list)


if __name__ == '__main__':
    main()