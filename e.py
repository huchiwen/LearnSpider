import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import csv
import img2pdf
import os
import time
import pprint
from bs4 import BeautifulSoup
import json


def page_code():
    a1 = 1
    page_num = 20
    page_size = 1001
    #total = page_size / page_num
    # data = {}
    data = []
    all_data = []

    for i in range(1, page_size):
        list_number = a1 + (i - 1) * page_num
        step = (list_number + page_num) - 1
        # data[i] = {list_number,step}
        data.append([list_number, step])
        # print(list_number,step)
    # print(data)
    return data

def get_api_params():

    urls = []
    for i in page_code():
        step = '-'.join([str(ii) for ii in i])
        url = f'https://qingarchives.npm.edu.tw/index.php?act=Archive//{step}'
        urls.append(url)
    return urls

def save_to_csv(self, fileName, mode, contents):

    with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in contents:
            writer.writerow(i)
            # print('数据保存成功.')

def get_page_data(headers,cookies,url):

        r = requests.get(url, headers=headers, cookies=cookies)
        #print(r.text)

        soup = BeautifulSoup(r.text, 'lxml')
        access_keys = soup.find_all("a", class_="act_content_display")
        accnum = soup.find(id='result_access_num').get('value')

        for access in access_keys:
            #data_list = [access.get('acckey'), accnum]
            #all_list.append(data_list)
            acckey = access.get('acckey')
            data = {
                'act': f'Display/initial/{acckey}/{accnum}'
            }
            rr = requests.post(url,headers=headers,cookies=cookies,data=data)
            print(rr.text)



def main():

    cookies = {
        'PHPSESSID': 'olukv0ldhcv0bu1ojg9qb59raj',
        '_ga': 'GA1.1.1303102741.1658115604',
        '_ga_91MJR5YCWN': 'GS1.1.1658115604.1.1.1658118253.0',
    }

    headers = {
        'authority': 'qingarchives.npm.edu.tw',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://qingarchives.npm.edu.tw',
        'referer': 'https://qingarchives.npm.edu.tw/index.php?act=Archive',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36,"',
        'x-requested-with': 'XMLHttpRequest',
    }
    urls =get_api_params()
    '''
    不知道为什么用多线程下载获取不到数据提示 overwrite，只能用单线程的办法去获取,但是，数据量太大。耗时间
    '''
    for url in urls:
        get_page_data(headers,cookies,url)

    '''    
    多线程获取不到数据
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = [executor.submit(get_page_data,headers,cookies,url) for url in urls]
        for future in as_completed(future_to_url):
            print(future.result())
    '''




if __name__ == '__main__':
    main()