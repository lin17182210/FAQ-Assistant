#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests

KEY = '4r9bergjetiv1tsd'  # API key
UID = "U785B76FC9"  # 用户ID
LOCATION = 'beijing'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
API = 'https://api.seniverse.com/v3/weather/now.json'  # API URL，可替换为其他 URL
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言


def fetch_weather(location):
    weather = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return weather.json()


if __name__ == '__main__':
    address = "杭州"
    result = fetch_weather(address)
    data = result.get("results")[0]
    addresses = data.get("location").get("name")
    print(addresses)
    print(data.get("now"))
