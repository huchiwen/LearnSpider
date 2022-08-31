import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from requests import exceptions 
import os
import time
import pprint
from bs4 import BeautifulSoup
import json
import json
import csv

class WebSpider:
      
    def __init__(self,cookies,headers):

        self.cookies = cookies
        self.headers = headers

    def page_code(self):
        a1 = 1 
        page_num = 20
        page_size = 446855
        total = page_size / page_num
        data = {}

        for i in range(1,page_size):
            list_number = a1 + (i -1) * page_num
            step =(list_number + page_num) - 1
            data[i] = {list_number,step} 
            data.update()
            #print(list_number,step)
        return data

    ''' https://www.pythontutorial.net/python-basics/python-write-csv-file/
        csv example
    '''

    def save_to_csv(self,fileName,mode,contents):

        fields = ['acckey', 'accnum']
        #print(onehead)
        with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
             writer = csv.DictWriter(f, fieldnames = fields) 
             #writer.writeheader()
             writer.writerows(contents)
             print('数据保存成功.')

    #get the acckey and accnum,after save into data file
    def get_acckey_and_accnum(self):

        access_keys = {}
        accnum = {}
        fileName = 'data'
        data_list = []
        dicts = {}
        onehead = 0
        t1 = time.time()
        for k,v in self.page_code().items():
            step = '-'.join([str(i) for i in v])
            url = f'https://qingarchives.npm.edu.tw/index.php?act=Archive//{step}'
            #print(url)
            #print('-'.join([str(i) for i in v]))
            r = requests.get(url,cookies=self.cookies,headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')

            access_keys = soup.find_all("a", class_="act_content_display")
            accnum = soup.find(id='result_access_num').get('value')

            for access in access_keys:
                dicts = {'acckey':access.get('acckey'),'accnum':accnum}
                dicts.update(dicts)
                data_list.append(dicts)
                #self.save_to_csv('data','a+',data_list)
                '''
                t2 = time.time()
                t  = t2 - t1
                print(f'running time:{t}')
                '''

if __name__ == '__main__':

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
    
    obj =  WebSpider(cookies,headers)
    with ThreadPoolExecutor(max_workers=20) as pool:
         pool.submit(obj.get_acckey_and_accnum)
