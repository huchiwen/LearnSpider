import requests
from requests import exceptions 
import os
import time
import pprint
from bs4 import BeautifulSoup
import json

def get_data(cookies,headers):

    url = 'https://qingarchives.npm.edu.tw/index.php?act=Archive'

    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.text, 'lxml')

    access_keys = soup.find_all("a", class_="act_content_display")
    accnum = soup.find(id='result_access_num').get('value')

    #print(access_keys,accnum)

    result = {}
    page_data = {}
    new_page_data = {}
    download_failure_file = {}

    for access in access_keys:
        access_key = access.get('acckey')
        data = {
            'act': f'Display/initial/{access_key}/{accnum}',
        }
        root_url = 'https://qingarchives.npm.edu.tw/index.php'
        # print(data)
        r = requests.post(root_url, cookies=cookies, headers=headers, data=data)
        #print(r.text)
        data = r.json().get('data')
        display = data.get('display')
        resouse = data.get('resouse')
        
        url2 = f'https://qingarchives.npm.edu.tw/index.php?act=Display/{display}/{resouse}'
        
        data2 = {
            'act': f'Display/built/{resouse}/jpg'
        }
        rr = requests.post(root_url, cookies=cookies, headers=headers, data=data2)
        result = rr.json()
        
        json_data = result.get('data')
        page_filename = json_data.get('page_filename')
        
        # page_thumb = json_data.get('page_thumb').values()
        page_thumb = json_data.get('page_thumb')
        page_list = json_data.get('page_list')

        new_dicts = merge_dict(page_thumb,page_list)
        page_data = {resouse:new_dicts}
        #print(page_data)
        new_page_data.update(page_data)
    return new_page_data

'''
合并两个字典,重新构造一个新的字典,构建新的对应关系
'''
def merge_dict(page_thumb,page_list):
    
    page_data = {}
    #合并两个字典,重新构造一个新的字典,构建新的对应关系
    for k,v in page_thumb.items():
        for kk,vv in page_list.items():
            if k == kk:
               page_data.update({v:vv})
    return page_data


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
    rr = get_data(cookies,headers)
    '''
    pp = pprint.PrettyPrinter(width=41, compact=True)
    pp.pprint(rr)
    '''
    
    # make a dir
    dirs = 'imgs'
    if not os.path.exists(dirs):
        os.mkdir(dirs)

    #download jpg file 
    for k,v in rr.items():
        for kk,vv in v.items():
            #download_jpg(k,kk,vv,dirs,cookies,headers)
            with open(f'{dirs}/{kk}','wb') as f:
                 jpg_url =f'https://qingarchives.npm.edu.tw/index.php?act=Display/loadimg/{k}/{vv}'
                 #print(jpg_url)
                 #请求必须要带 cookies 和headers ,直接用上面的网址是访问不到的,会出现一个读图图片失败的页面
                 jpg_file = requests.get(jpg_url,cookies=cookies,headers=headers)

                 if jpg_file.status_code == 200:
                    f.write(jpg_file.content) 
                    print(f'file name: {kk} was already save into {dirs} directory.')
#用不上这个方法
def save_to_file(data_dicts):
    with open('download_failure_file.csv') as ff:
        f.write(data_dicts)
        print(f'下载失败的文件已经保存到download_failure_file.csv文件中')

if __name__ == '__main__':
    main()
