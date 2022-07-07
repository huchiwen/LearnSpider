import requests
import re
from bs4 import BeautifulSoup
import time

def get_data():
    url = "http://42.194.197.95:8001/poison_url"
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6",
        "Cache-Control":"no-cache",
        "Cookie":"session=.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.YsQY7w.T9qY6fSOFbW2IT4Je1LhYFzFCkg; auth=580EEETT353480BWR1657020793",
        "Host":"42.194.197.95:8001",
        "Pragma":"no-cache",
        "Proxy-Connection":"keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",

    }

    r = requests.get(url=url,headers=headers)
    #print(r.text)
    soup = BeautifulSoup(r.text,'lxml')
    movie_list = soup.find('div',class_='movie-list').find_all('a',class_='list-group-item')
    result = []
    for img_list in movie_list:
        movieImage = img_list.find('p').find_next_sibling('p').get_text()
        #print(movieImage)
        result.append(movieImage)
    return result

def remove_list(key,list_key):
    result = []
    for li in list_key:
        if li != key:
            result.append(li)
    return result

def make_list(data_list, remove_str):
        return [x for x in data_list if remove_str != x]  # this will change the original list
            
def main():

    remove_str= 'http://42.194.197.95:8001/poison_img_url'
    page_list = get_data()

    t1 = time.time()
    a =make_list(page_list,remove_str)
    t2 = time.time()
    print(t2-t1)

if __name__ =='__main__':
    main()
