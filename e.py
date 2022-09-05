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



''' 
  该代码可以用多线程爬虫acckey 和accnum 但是数据量不对,网站是1000 页 每页20 条数据,对应的acckey 和accnum 是2w个

'''

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


'''多个字段保存'''
def save_to_csv(fileName, mode, contents):

    with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in contents:
            writer.writerow(i)
            #print('数据保存成功~~')

''' 列表单个字段保存'''
def save_single_string_csv(fileName, mode, contents):

    with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(contents)
        print('数据保存成功.')

def get_acckey_accnum(headers,url):

        data_list = []
        all_list = []
        r = requests.Session()
        response = r.get(url, headers=headers)
        print(url)

        soup = BeautifulSoup(response.text, 'lxml')
        access_keys = soup.find_all("a", class_="act_content_display")
        accnum = soup.find(id='result_access_num').get('value')

        for access in access_keys:
            data_list = [access.get('acckey'), accnum]
            all_list.append(data_list)
        #print(all_list)
        return all_list
            
            
     
def get_page_data(headers,url):

        '''
        data_list = []
        r = requests.Session()
        response = r.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        access_keys = soup.find_all("a", class_="act_content_display")
        accnum = soup.find(id='result_access_num').get('value')

        for access in access_keys:
            #data_list = [access.get('acckey'), accnum]
            #all_list.append(data_list)
            acckey = access.get('acckey')
            data = {
                'act': f'Display/initial/{acckey}/{accnum}'
            }
            rr = r.post(url,headers=headers,data=data)
            data = [rr.json().get('data').get('resouse')]
            data_list.append(data)
            #print(data_list)
        return data_list
      '''
'''
多线程获取不到数据

获取不到数据的问题已经解决了,(共用会话 ID 导致的),详细说明在下面这个地址
https://segmentfault.com/q/1010000042428840?_ea=264572510
'''
def get_resouse(urls,headers):

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = [executor.submit(get_acckey_accnum,headers,url) for url in urls]
        for future in as_completed(future_to_url):
            data = future.result()
            #print(data)
            save_to_csv('data','a+',data)
            #print(resouse)

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
      不知道为什么用多线程下载获取不到数据提示 overwrite,原因是共用一个ssession 用requests.Session()可以解决
      现在单线程获取acckey 和accnum 成功,多线程遇到网站反爬,导致,获取到一部分数据就获取不了,解决办法是用钱买代理ip(这个技术还没有用)
      多线程代码已经完成了,只是遇到网站反爬,导致数据获取不完全.
    '''
    for url in urls:
        data = get_acckey_accnum(headers,url)
        save_to_csv('data','a+',data)

    '''
    if os.path.exists('resouse.csv'):
        print('读取本地的resouse.csv文件(未开发).....')
        
    else:
        print('开始去网站爬取acckey 和accnum,保存到本地的data.csv')
        get_resouse(urls,headers)
    '''


if __name__ == '__main__':
    main()
