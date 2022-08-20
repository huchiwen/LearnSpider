import requests
from requests import exceptions 
import os
import time
import pprint
from bs4 import BeautifulSoup
import json
import threading

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



    # save to file
    def save_to_file(self,fileName,content):
        with open('{fileName}.csv','wb') as ff:
             ff.write(fileName)
             print(f'文件已经保存到{fileName}.csv文件中')

    #get the acckey and accnum,after save into data file
    def get_acckey_and_accnum(self):

        access_keys = {}
        accnum = {}

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
                 #print(access.get('acckey'),accnum)
                 contents = {access.get('acckey'):accnum}
                 contents.update(contents)
                 print(url,contents)
        self.save_to_file('data',contents)

        '''
        r = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(r.text, 'lxml')

        self.access_keys = soup.find_all("a", class_="act_content_display")
        self.accnum = soup.find(id='result_access_num').get('value')

        #print(self.access_keys,self.accnum)
				
        for access in self.access_keys:
            access_key = access.get('acckey')
            data = {
                'act': f'Display/initial/{access_key}/{self.accnum}',
            }
            root_url = 'https://qingarchives.npm.edu.tw/index.php'
            # print(data)
            r = requests.post(root_url, cookies=cookies, headers=headers, data=data)
            print(r.text)
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
    for i in range(10000):
        t = threading.Thread(target=obj.get_acckey_and_accnum)
        t.start()
        t.join()

