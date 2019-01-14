import requests
import json
import time
import random
from agent_helper import get_random_agent
import sqlalchemy_helper

# 取页面HTML
def get_one_page(url):
    agent = get_random_agent()
    print(agent)

    headers = {
        'Referer': 'https://list.mogujie.com/s?q=%E9%9E%8B%E5%AD%90&ptp=1.mqKfub.0.0.pIFtt39L',
        'User-Agent': agent,
        'Host': 'list.mogujie.com',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None

def parse_page(html):
    i = html.index('(')
    html = html[i+1:]
    html = html[:-2]
    result_dict = json.loads(html)
    # print(result_dict)
    is_end = result_dict['result']['wall']['isEnd']
    if is_end:
        return None

    results = result_dict['result']['wall']['docs']
    result_list = []
    for item in results:
        item_dict = {}
        item_dict['tradeItemId'] = item.get('tradeItemId', '')
        item_dict['itemType'] = item.get('itemType', '')
        item_dict['img'] = item.get('img', '')
        item_dict['clientUrl'] = item.get('clientUrl', '')
        item_dict['link'] = item.get('link', '')
        item_dict['itemMarks'] = item.get('itemMarks', '')
        item_dict['acm'] = item.get('acm', '')
        item_dict['title'] = item.get('title', '')
        item_dict['cparam'] = item.get('cparam', '')
        item_dict['orgPrice'] = item.get('orgPrice', '')
        item_dict['hasSimilarity'] = item.get('hasSimilarity', '')
        item_dict['sale'] = item.get('sale', '')
        item_dict['cfav'] = item.get('cfav', '')
        item_dict['price'] = item.get('price', '')
        item_dict['similarityUrl'] = item.get('similarityUrl', '')

        result_list.append(item_dict)
    return result_list

def write_json(result_list):
    html_str = json.dumps(result_list, ensure_ascii=False)

    with open('./mogujie.json', 'a') as f:
        f.write(html_str)

def main():
    page = 1
    while (True):
        url = 'https://list.mogujie.com/search?callback=jQuery21108307139015410421_1543376477667&_version=8193&ratio=3%3A4&cKey=15&page=' + str(page) + '&sort=pop&ad=0&fcid=50330&action=shoes&acm=3.mce.1_10_1jxc6.128038.0.5fV4draFaldTp.pos_4-m_464807-sd_119&ptp=1.n5T00.0.0.4pF9qC5C&_=1543376477669'
        
        # time.sleep(1)
        html = get_one_page(url)
        if '(' not in html:
            print('.......in error.......')
            # t = random.randint(1, 3)
            # time.sleep(t)
            continue

        print(html)
        # print(html)
        result_list = parse_page(html)

        if result_list is None:
            break

        print(page, len(result_list))
        sqlalchemy_helper.save_db(result_list)

        write_json(result_list)

        page += 1

if __name__ == '__main__':
    main()