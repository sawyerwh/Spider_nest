#!/usr/bin/python3
# coding=utf-8
import re
import json
import requests


def get_page(url):
    """获取页面HTML"""
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    # 如果页面响应码为200(访问成功)
    if response.status_code == 200:
        # 返回页面内容(字节流)
        return response.content.decode('utf-8')
    return None


def parse_page(html):
    """解析页面（正则）"""
    pattern = re.compile(
        'movieId.*?>(.*?)</a>.*?<div class="channel-detail channel-detail-orange">(.*?)</div>', re.S
        )
    items = re.findall(pattern, html)
    # print(items)
    movies = []
    for item in items:
        # print(item)
        movie = {}
        if len(item[1]) != 4:
            pattern1 = re.compile(
                '<i class="integer">(.*?)</i><i class="fraction">(.*?)</i>', re.S
                )
            # print(item[1])
            item1 = re.findall(pattern1, item[1])
            # print(item1)
            movie['name'] = item[0]
            movie['score'] = str(item1[0][0]) + str(item1[0][1])
            movies.append(movie)
        else:
            movie['name'] = item[0]
            movie['score'] = item[1]
            movies.append(movie)
    return movies


def save_json(result):
    """保存为 json 文件"""
    json.dumps(result, ensure_ascii=False)
    with open('./json/regular_movies.json', 'w', encoding='utf-8')as file:
        file.write(result)
        print('写入json文件成功')


def main():
    """主函数"""
    url = 'https://maoyan.com/films'
    html = get_page(url)
    result = str(parse_page(html))
    save_json(result)


if __name__ == '__main__':
    main()
