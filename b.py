import requests
import time
import pprint
from bs4 import BeautifulSoup
import json

# data: {act: 'Display/initial/' + access_key + '/' + accnum},
def send_post_request(url,cookies, header, form_data):
    r = requests.post(
        url,
        cookies=cookies,
        headers=header,
        data=form_data
    )
    result_data = r.json()
    return result_data

def get_api_data(url,headers,cookies):

    r = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(r.content, 'lxml')

   # with open('/Users/apple/LearnSpider/aa.html','wb') as f:
   #       f.write(r.content)
   #     

    # get acckey
    access_key = soup.find_all("a",class_="act_content_display")
    accnum = soup.find(id='result_access_num').get('value')
    print(len(access_key))
    exit()

    acckey_list = []
    all_list = {}
    index = 0

    for access in access_key:
        print(access.get('acckey'))
        #access_key_list = access.get('acckey')
        #data ={
        #    'act': f'Display/initial/{access_key_list}/{accnum}',
        #}
        #index = index + 1
        '''
        all_list[index] = send_post_request(url,cookies,headers,data)
        index = index + 1
    return all_list
        '''


'''
content-length 导致返回的数据很慢才出结果,
建议取消掉,cookies 也要记得传,
不传会导致接口请求成功,但是,获取不到数据
'''
def main():

        headers = {
            "authority":"qingarchives.npm.edu.tw",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://qingarchives.npm.edu.tw",
            "referer": "https://qingarchives.npm.edu.tw/index.php?act=Archive",
            "sec-ch-ua": '.Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        cookies ={
            'PHPSESSID':'e83ajkt47ph951etmo3954duru',
            '_ga':'GA1.1.247714735.1658044299',
            '_ga_91MJR5YCWN':'GS1.1.1658131250.6.1.1658131402.0',

        }

        url = 'https://qingarchives.npm.edu.tw/index.php'
        url_for_get = 'https://qingarchives.npm.edu.tw/index.php?act=Archive'

        r = requests.get(url_for_get,headers=headers,cookies=cookies)
        soup = BeautifulSoup(r.text,'lxml')

        access_keys = soup.find_all("a",class_="act_content_display")
        print(len(access_keys))
       

if __name__ == '__main__':
    main()
