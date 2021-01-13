#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests

MY_KEY = '&key=584bfd5ea6b947fcb0144c5b87696757'  # EDIT HERE!
URL_API_WEATHER = 'https://devapi.qweather.com/v7/weather/3d'
URL_API_GEO = 'https://geoapi.qweather.com/v2/city/'


def fetch_weather(city, key, slot):
    url = URL_API_WEATHER + '?location=' + city + key
    weather_data = requests.get(url).json()
    result = weather_data.get("daily")[slot]
    day = result.get("fxDate")
    text_day = result.get("textDay")
    temp_max = result.get("tempMax")
    temp_min = result.get("tempMin")
    text_night = result.get("textNight")
    text_template = """[{}] 的天气情况为: 白天{}, 夜晚{}, 最高温度{}度, 最低温度{}度.""". \
        format(day, text_day, text_night, temp_max, temp_min)
    return text_template


def fetch_city(city, key):
    url_v2 = URL_API_GEO + 'lookup?location=' + city + key
    city = requests.get(url_v2).json()['location'][0]
    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']
    lat = city['lat']
    lon = city['lon']
    return city_id, district_name, city_name, province_name, country_name, lat, lon


def fetch(city, day, key=MY_KEY):
    city_info = fetch_city(city, key)
    city_id = city_info[0]
    day_slot = {
        "明天": 1,
        "后天": 2
    }
    message = fetch_weather(city_id, key, day_slot.get(day, 0))
    if city_info[2] == city_info[1]:
        message = "".join([city_info[3], str(city_info[2]), '市', message])
    else:
        message = "".join([city_info[3], str(city_info[2]), '市', str(city_info[1]), '区', message])
    return message


if __name__ == '__main__':
    CITY_INPUT = "杭州"
    print(fetch(CITY_INPUT, "后天"))
