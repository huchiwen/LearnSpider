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
    # print(r.text['data']['resouse'])
    print(r.json())
    # result_data = r.json()
    # print(result_data)
    # return result_data


def get_accnum_and_acckey(url,headers,cookies):

    response = requests.get(url,headers=headers,cookies=cookies,params={'act': 'Archive'})
    soup = BeautifulSoup(response.text, 'lxml')


    # get acckey
    acckey_list = []
    #num_list = []
    access_key = soup.find_all('a',class_='act_content_display')
    accnum = soup.find(id='result_access_num').get('value')

    for access in access_key:
        #print(access.get('acckey'))
        access_key_list = access.get('acckey')
        data ={
            'act': f'Display/initial/{access_key_list}/{accnum}',
        }
        send_post_request(url,cookies,headers,data)

'''
content-length 导致返回的数据很慢才出结果,建议取消掉,cookies 也要记得传,不传会导致接口请求成功,但是,获取不到数据
'''

def main():

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6",
            #"content-length": "49",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            #"cookie": "PHPSESSID=lr90bcpfbi2m431h2us7q8s41a; _ga=GA1.1.229769402.1657931243; _ga_91MJR5YCWN=GS1.1.1657957371.5.1.1657957418.0",
            "cookie":"PHPSESSID=lr90bcpfbi2m431h2us7q8s41a; _ga=GA1.1.229769402.1657931243; _ga_91MJR5YCWN=GS1.1.1657985250.7.1.1657985294.0",
            "origin": "https://qingarchives.npm.edu.tw",
            "referer": "https://qingarchives.npm.edu.tw/index.php?act=Display/image/217344HTN0=Fg",
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
            '_ga_91MJR5YCWN':'GS1.1.1658131250.6.1.1658131402.0',
            '_ga':'GA1.1.247714735.1658044299',

        }

        url = 'https://qingarchives.npm.edu.tw/index.php'
        data = {
            'act': 'Display/built/217344HTN0=Fg/dal/jpg'
        }
        result = get_accnum_and_acckey(url,headers,cookies)

        accnum = list(result.keys())[0]


        for i in range(len(result[accnum])):
            data = {
                'act': 'Display/initial/' + result[accnum][i] + '/' + accnum
            }
            print(data)
            response_data = send_post_request(url,cookies, header, data)

if __name__ == '__main__':
    main()
