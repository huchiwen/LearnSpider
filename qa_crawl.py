import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import pprint
from bs4 import BeautifulSoup
import csv
import os


class WebSpider(threading.Thread):

    def __init__(self, cookies, headers):

        self.cookies = cookies
        self.headers = headers

    def page_code(self):
        a1 = 1
        page_num = 20
        page_size = 1001
        total = page_size / page_num
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

    ''' 
    https://www.pythontutorial.net/python-basics/python-write-csv-file/
    csv example
    '''

    def save_to_csv(self, fileName, mode, contents):

        with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
            writer = csv.writer(f)
            for i in contents:
                writer.writerow(i)
                # print('数据保存成功.')

    def get_api_params(self):

        urls = []

        for i in self.page_code():
            step = '-'.join([str(ii) for ii in i])
            url = f'https://qingarchives.npm.edu.tw/index.php?act=Archive//{step}'
            urls.append(url)
        return urls

    def get_acckey_and_accnum(self,url):
        data_list = []
        all_list = []
        r = requests.get(url,headers=self.headers,cookies=self.cookies)
        print(r.cookies)
        soup = BeautifulSoup(r.text, 'lxml')

        access_keys = soup.find_all("a", class_="act_content_display")
        accnum = soup.find(id='result_access_num').get('value')

        for access in access_keys:
            data_list = [access.get('acckey'), accnum]
            all_list.append(data_list)
            print("download url {} finished at {}".format(urls, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        return all_list

    '''
        利用线程池去获取acckey 和accnum的值，保存到csv文件中.
    '''

    def saveAcckey2cvs(self, cookies, headers, urls):

        '''
        for i in urls:
            data = obj.send_get_request(i)
            #print(data)
            obj.save_to_csv('data','a+',data)
        '''
        ''' 
            python3 线程学习网站
            https://cloud.tencent.com/developer/article/1597890
        '''
        executor = ThreadPoolExecutor(max_workers=20)
        all_task = [executor.submit(obj.get_acckey_and_accnum, (url)) for url in urls]

        for task in as_completed(all_task):
            data = task.result()
            #print(data)
            # print("任务 {} down load success".format(data))
            obj.save_to_csv('data', 'a+', data)
            # print(f"{data}数据保存成功")
    '''
    这个方法是获取不到接口的数据,想要获取到数据请查看e.py文件的写法
    '''
    def get_page_api_data(self,headers,cookies):

        with open("data.csv", mode="r", encoding="utf-8") as ff:
            read = csv.reader(ff)
            for i in read:
                # print(i[0],i[1])
                data = {
                    'act':f'Display/initial/{i[0]}/{i[1]}'
                }
                root_url = 'https://qingarchives.npm.edu.tw/index.php'
                r = requests.post(root_url,cookies=cookies,headers=headers,data=data)
                print(r.text)

if __name__ == '__main__':

    cookies = {
        'PHPSESSID':'olukv0ldhcv0bu1ojg9qb59raj',
        '_ga':'GA1.1.1303102741.1658115604',
        '_ga_91MJR5YCWN':'GS1.1.1658115604.1.1.1658118253.0',
    }
    headers = {
        'authority':'qingarchives.npm.edu.tw',
        'accept':'application/json, text/javascript, */*; q=0.01',
        'accept-language':'zh-CN,zh;q=0.9',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'origin':'https://qingarchives.npm.edu.tw',
        'referer':'https://qingarchives.npm.edu.tw/index.php?act=Archive',
        'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'macOS',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36,"',
        'x-requested-with':'XMLHttpRequest',
    }
    obj = WebSpider(cookies, headers)
    urls = obj.get_api_params()
    #print(urls)
    #local_data = obj.saveAcckey2cvs(cookies,headers,urls)

    if os.path.exists('data.csv'):
        print('读取本地的data.csv,获取acckey和accnum')
        local_data = obj.get_page_api_data(cookies, headers)
    else:
        print('开始去网站爬取acckey 和accnum....')
        obj.saveAcckey2cvs(cookies, headers, urls)
