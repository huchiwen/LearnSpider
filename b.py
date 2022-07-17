import requests
import time
import pprint
from bs4 import BeautifulSoup
import json

header = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6",
    "content-length": "49",
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


# data: {act: 'Display/initial/' + access_key + '/' + accnum},


# print(r.text)
def send_post_request(url, header, form_data):
    r = requests.post(
        url,
        headers=header,
        data=form_data
    )
    # print(r.text['data']['resouse'])
    print(r.json())
    # result_data = r.json()
    # print(result_data)
    # return result_data


def get_accnum_and_acckey(url):
    response = requests.get(url, params={'act': 'Archive'})
    # print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    #print(soup)

    element_name = {
        "id": "result_access_num"
    }
    # 获取 access_num
    access_num = soup.find('input', element_name)['value']
    # print(access_num)

    # get acckey
    acckey_list = []
    num_list = []
    for items in soup.find_all('div', attrs={'class': 'data_record'}):
        result_title = items.find('div', attrs={'class': 'result_title'})
        num = items.find('span', attrs={'class': 'meta_num'}).text.replace(".", " ")
        num_list.append(num)
        acckey_list.append(result_title.a['acckey'])

    # print(acckey_list,access_num)

    # access_num = access_num.split(" ")
    # access_num = access_num * len(acckey_list)
    # print(access_num,acckey_list)
    dd = {access_num: acckey_list}
    return dd


def main():

        url = 'https://qingarchives.npm.edu.tw/index.php'
        data = {
            'act': 'Display/built/217344HTN0=Fg/dal/jpg'
        }
        result = get_accnum_and_acckey(url)

        accnum = list(result.keys())[0]


        for i in range(len(result[accnum])):
            data = {
                'act': 'Display/initial/' + result[accnum][i] + '/' + accnum
            }
            print(data)
            response_data = send_post_request(url, header, data)

if __name__ == '__main__':
    main()
