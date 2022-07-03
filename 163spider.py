import requests
import json
from openpyxl import Workbook
from datetime import datetime


def main():
    url = 'https://study.163.com/p/search/studycourse.json'

    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",

    }
    playload = {
        "activityId": 0,
        "keyword": "c++",
        "orderType": 50,
        "pageIndex": 1,
        "pageSize": 50,
        "relativeOffset": 0,
        "priceType": -1,
        "qualityType": 0,
        "searchTimeType": -1,
        "searchType": 40,
        "vipSearchType": -1
    }

    r = requests.post(url, headers=header, json=playload)
    result = r.json()
    data = result['result']['list']
    for data_list in data:
        data_tuple = (
            data_list['productId'], data_list['courseId'], data_list['productName'],
            data_list['provider'], data_list['score'], data_list['learnerCount'], data_list['lessonCount'],
            data_list['originalPrice'], data_list['discountRate'], data_list['vipPrice'])
        save_to_excel(data_tuple)
        # print(data_tuple)


def save_to_excel(input_data):
    ws.append(input_data)


if __name__ == '__main__':
    title = ['商品id', '课程id', '课程名称', '机构名称', '评分', '学习人数', '课程节数', '原价', '折扣价', '会员价格']
    wb = Workbook()
    ws = wb.active
    ws.append(title)
    main()
    wb.save(f'course_info_{datetime.now()}.xlsx')
