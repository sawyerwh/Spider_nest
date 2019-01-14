#!/usr/bin/python3
# coding=utf-8
import requests
import json
import pymysql


# 获取页面html
def get_one_page(url):

        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            text = response.content.decode('utf-8')
            return text
        return None


# 获取目标json数据
def get_real_content(html):
    if html and len(html) >128:
        i = html.index('(')
        html1 = html[i+1:]
        html2 = html1.replace(');', '')
        return html2
    return None


# 提取需求信息集合
def parse_one_page(result1):
    skirts = []
    for item in result1:
        skirt = {}
        skirt['tradeItemId'] = item['tradeItemId']
        skirt['itemType'] = item['itemType']
        skirt['img'] = item['img']
        skirt['itemMarks'] = item['itemMarks']
        skirt['title'] = item['title']
        skirt['orgPrice'] = item['orgPrice']
        skirt['sale'] = item['sale']
        skirt['cfav'] = item['cfav']
        skirt['price'] = item['price']
        skirts.append(skirt)
    return skirts


# 保存数据库
def save_data(skirts):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'spider01'
    port = 3306
    db = pymysql.connect(host, user, password, database, port)
    cursor = db.cursor()
    for skirts_data in skirts:

        data1 = (skirts_data['title'],skirts_data['tradeItemId'],skirts_data['orgPrice'],skirts_data['price'],skirts_data['sale'],skirts_data['cfav'],skirts_data['itemType'],skirts_data['itemMarks'],skirts_data['img'])
        sql = "insert into mogu_skirts(title,tradeItemId,orgPrice,price,sale,cfav,itemType,itemMarks,img) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"% data1
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    db.close()


def main():
    # 循环刷新页面地址
    page_i = 0
    while True:
        page_i += 1
        url = "https://list.mogujie.com/search?callback=jQuery211042073306521965237_1540373720760&_version=8193&ratio=3%3A4&cKey=15&page=" + str(page_i) + "&sort=pop&ad=0&fcid=50004&action=skirt&acm=3.mce.1_10_1hddc.109520.0.bYOWZr7menQUh.pos_0-m_405212-sd_119-mf_15261_1047900-idx_0-mfs_16-dm1_5000&ptp=1._mf1_1239_15261.0.0.VfaUcI3J&_"

        # 获取页面字节流
        html = get_one_page(url)
        # 获取目标json数据
        html_content = get_real_content(html)
        # 将json解析成python 字典
        result = json.loads(html_content)
        # 获取内部目标商品集合
        result1 = result['result']['wall']['docs']
        # 提取需求信息集合
        skirts = parse_one_page(result1)
        # 保存数据库
        print(len(skirts))
        save_data(skirts)
        # 控制台提示
        print('成功爬取保存一页')

        # 获取页面isEnd 参数
        flag = result['result']['wall']['isEnd']
        # 判断抓取页面是否为最后一页（isEnd==True）
        if flag:
            break

    print('完毕！！')


if __name__ == '__main__':
    main()
