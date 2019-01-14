import requests
from lxml import etree
import pymysql
import threading


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
def save_data(one_page_names):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'name_all'
    port = 3306
    db = pymysql.connect(host, user, password, database, port)
    cursor = db.cursor()
    for item in one_page_names:
        data1 = (item['first_name'], item['name'], item['means'])
        sql = "insert into names(first_name,name,means) values ('%s','%s','%s')" % data1
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()
    print('保存一个姓氏')


def get_db_data():
    db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='name_all', port=3306)
    cursor = db.cursor()
    cursor.execute('select first_names, first_names_link from first_names')
    first_names_list = cursor.fetchall()
    db.close()
    return first_names_list


def get_thread_url():
    first_names_list = get_db_data()
    n = 15
    urls_list = [first_names_list[i:i + n] for i in range(0, len(get_db_data()), n)]
    return urls_list


def main(item):
    # print(item)
    for i in item:
        # 获取当前 姓氏名称  后期存字典
        first_name = i[0]
        # 获取当前 姓氏url（不完整）
        item1 = i[1]
        # 第二层 姓氏url 补全
        url = 'http:' + item1
        url01 = url.split('.html', 1)[0]

        # 第二层 分页 共 10页
        one_first_names = []
        for j in range(1, 11):
            url02 = url01 + '_%s.html' % j
            # 第二层 页面获取 html
            html01 = get_one_page(url02)
            # 第二层 页面解析 获取 姓名 及 第三层链接
            result = parse_name_detail(html01)


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
            save_data(one_page_names)

        print('爬取一个姓氏')

    print('完成')


if __name__ == '__main__':
    first_names = get_thread_url()
    threads = []
    for item in first_names:
        t1 = threading.Thread(target=main, args=(item,))
        threads.append(t1)
        t1.start()
    # 等子线程结束
    for t1 in threads:
        # 阻塞线程，当t1执行完时 再执行
        t1.join()
    print('线程全部启动')