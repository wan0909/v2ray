#!/usr/bin/env python3

from datetime import timedelta, datetime
import json, re
import requests
from requests.adapters import HTTPAdapter

# 文件路径定义
list_path = './list.json'

with open(list_path, 'r', encoding='utf-8') as f: # 载入订阅链接
    raw_list = json.load(f)
    f.close()

def url_updated(url): # 判断远程远程链接是否已经更新
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    try:
        resp = s.get(url, timeout=2)
        status = resp.status_code
    except Exception:
        status = 404
    if status == 200:
        url_updated = True
    else:
        url_updated = False
    return url_updated

class update():

    def main():
        for item in raw_list:
            id = item['id']
            current_url = item['url']
            try:
                if item['update_date'] == True:
                    print(f'Finding available update for ID{id}')
                    new_url = update.change_date(id,current_url)
                    if new_url == current_url:
                        print(f'No available update for ID{id}\n')
                    else:
                        item['url'] = new_url
                        print(f'ID{id} url updated to {new_url}\n')
            except KeyError:
                print(f'{id} Url not changed! Please define update method.')

            updated_list = json.dumps(raw_list, sort_keys=False, indent=2, ensure_ascii=False)
            file = open(list_path, 'w', encoding='utf-8')
            file.write(updated_list)
            file.close()

    # 更新 url 最后一个 / 后的日期，比如 https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/0000.txt 中的 0000
    def change_date(id,current_url):
        today = datetime.today().strftime('%m%d')
        url_front = current_url[0:current_url.rfind('/', 1) + 1]
        url_end = current_url.split('/')[-1].split('.')[-1]
        new_url = url_front + today + '.' + url_end

        if url_updated(new_url):
            return new_url
        else:
            return current_url