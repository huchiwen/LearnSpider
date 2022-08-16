import requests
import img2pdf
import os
import time
import pprint
from bs4 import BeautifulSoup
import json

'''
 这是一个练手的爬虫项目,
 程序原理: 回去accnum,acckeys 提交到指定的接口,返回数据,在请求第二个接口返回jpd 的图片地址,再保存成pdf(保存pdf功能还没有实现)o


 遇到的问题是
 请求的没有带cookies 导致请求成功,没有数据返回 提示session overwrite
 请求的cookies 没有设置正确导致acceskeys 获取到40条,网站本来就20 条数据
 解决办法是在chrome 的cookies 插件 先把原来的cookies 删除掉,在重新访问,把获取到的PHPSSIONID,添加到代码的cookies即可.

'''

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

url = 'https://qingarchives.npm.edu.tw/index.php?act=Archive'
r = requests.get(url, headers=headers, cookies=cookies)

soup = BeautifulSoup(r.text, 'lxml')

access_keys = soup.find_all("a", class_="act_content_display")
accnum = soup.find(id='result_access_num').get('value')

# print(len(access_keys))

dirs = 'imgs'
dicts_filename = {}
pdf_dict = {}
thumb_list = {}
r_data = {}
if not os.path.exists(dirs):
    os.mkdir(dirs)

for access in access_keys:
    access_key = access.get('acckey')
    data = {
        'act': f'Display/initial/{access_key}/{accnum}',
    }

    root_url = 'https://qingarchives.npm.edu.tw/index.php'
    # print(data)

    r = requests.post(root_url, cookies=cookies, headers=headers, data=data)
    # print(r.text)

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

    #page_thumb = json_data.get('page_thumb').values()
    page_thumb = json_data.get('page_thumb')
    page_list = json_data.get('page_list')

    #dicts_filename = {'filename': page_thumb.values(), 'page_list': page_list.values(), 'resouse': resouse}
    for k,v in page_thumb.items():
        for kk,vv in page_list.items():
            if k == kk :
               thumb_list.update({v:vv})
    r_data = {resouse:thumb_list}

    for d_index,d_values in r_data.items():
        for didx,dval in d_values.items():
            with open(f'{dirs}/{didx}','wb') as f:
                 jpg_url =f'https://qingarchives.npm.edu.tw/index.php?act=Display/loadimg/{d_index}/{dval}'
                 #请求必须要带 cookies 和headers ,直接用上面的网址是访问不到的,会出现一个读图图片失败的页面
                 jpg_file = requests.get(jpg_url,cookies=cookies,headers=headers)
                 f.write(jpg_file.content) 
                 print(f'{didx} 文件下载完成.')
