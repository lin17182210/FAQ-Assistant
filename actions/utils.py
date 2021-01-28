#!/usr/bin/python
# -*- coding:utf-8 -*-
from typing import Text, List
import requests

MY_KEY = ''  # EDIT HERE!
URL_API_WEATHER = 'https://devapi.qweather.com/v7/weather/3d'
URL_API_GEO = 'https://geoapi.qweather.com/v2/city/'


def fetch_weather(city: Text, key: Text, slot: int) -> Text:
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


def fetch_city(city: Text, key: Text) -> List[Text]:
    url_v2 = URL_API_GEO + 'lookup?location=' + city + key
    city = requests.get(url_v2).json()['location'][0]
    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']
    lat = city['lat']
    lon = city['lon']
    return [city_id, district_name, city_name, province_name, country_name, lat, lon]


def fetch(city: Text, day: Text, key: Text = MY_KEY) -> Text:
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


def fetch_intent_description(intent_list: List[Text]) -> List[Text]:
    intent_dict = {
        "beikeUpdateToSchoolTimetable": "更新了备课模块是否会同步至课表",
        "courseCantComplete": "点播课章节无法完成",
        "examinationNoPermission": "没有权限查看考试",
        "lessonGarbledCode": "课堂中出现乱码",
        "ipadNoVoicedOnClass": "学生上课听不到老师的声音",
        "lockScreen": "如何锁定屏幕",
        "changeVoice": "如何变声",
        "authorizationFlipCourseware": "给学生授权后，课件是否可以翻页",
        "commentPaperNoExamination": "试卷讲评没有相关的考试",
        "cantMoveDiscussionArea": "移动讨论区",
        "cantloadCourseware": "平板上课件加载不出来",
        "noEnterClassButton": "平板进入课堂的按钮消失",
        "arrangeTemporarySchoolTimetable": "如何排临时课表",
        "ipadCantEnterClass": "平板无法进入课堂",
        "externalReleaseStudentVoice": "如何外放学生的声音",
        "connectMicrophoneNoVoice": "连麦没有声音",
        "examinationNoScore": "学生考试后没有成绩",
        "ipadEditQuestion": "平板是否可以编辑资源",
        "microcourseCantUpload": "微课无法上传",
        "whereMyCourseware": "上传课件后在我的资源里找不到",
        "microcourseFlashScreen": "微课录制出现闪退",
        "homeworkSelectErrorStudent": "修改作业选择的学生",
        "homeworkSelectError": "取消作业",
        "cantSelectPhotoHomework": "如何布置拍照作业",
        "howChangeHomeworkTime": "修改作业的时间",
        "whatIsHomeworkType": "作业类型",
        "ipadPrintPhoneticSymbols": "平板如何打出音标",
        "tipFixFlash": "修复flash",
        "videotapeCanAccelerate": "录像是否可以倍速播放",
        "cantChangeHeadPortrait": "无法修改头像"
    }
    intent_desc = [intent_dict.get(_) for _ in intent_list]
    return intent_desc


def entity_compile_intent(entities: List[Text]) -> List[Text]:
    entity_intent_dict = {
        "备课": ["beikeUpdateToSchoolTimetable"],
        "课表": ["beikeUpdateToSchoolTimetable"],
        "点播课": ["courseCantComplete"],
        "考试": ["examinationNoPermission", "commentPaperNoExamination", "examinationNoScore"],
        "课堂": ["lessonGarbledCode", "ipadNoVoicedOnClass", "noEnterClassButton", "ipadCantEnterClass",
               "connectMicrophoneNoVoice"],
        "乱码": ["lessonGarbledCode"],
        "平板": ["ipadNoVoicedOnClass", "cantloadCourseware", "noEnterClassButton", "ipadCantEnterClass",
               "ipadEditQuestion", "ipadPrintPhoneticSymbols"],
        "声音": ["ipadNoVoicedOnClass", "changeVoice", "externalReleaseStudentVoice", "connectMicrophoneNoVoice"],
        "屏幕": ["lockScreen"],
        "变声": ["changeVoice"],
        "锁屏": ["lockScreen"],
        "课件": ["authorizationFlipCourseware", "cantloadCourseware", "whereMyCourseware"],
        "试卷": ["commentPaperNoExamination"],
        "讨论区": ["cantMoveDiscussionArea"],
        "按钮": ["noEnterClassButton"],
        "临时课表": ["arrangeTemporarySchoolTimetable"],
        "连麦": ["connectMicrophoneNoVoice"],
        "成绩": ["examinationNoScore"],
        "习题": ["ipadEditQuestion"],
        "微课": ["microcourseCantUpload", "microcourseFlashScreen"],
        "闪退": ["microcourseFlashScreen"],
        "学生": ["ipadNoVoicedOnClass", "authorizationFlipCourseware", "externalReleaseStudentVoice",
               "examinationNoScore", "homeworkSelectErrorStudent"],
        "作业": ["homeworkSelectErrorStudent", "homeworkSelectError", "howChangeHomeworkTime", "whatIsHomeworkType"],
        "拍照作业": ["cantSelectPhotoHomework"],
        "时间": ["howChangeHomeworkTime"],
        "音标": ["ipadPrintPhoneticSymbols"],
        "flash": ["tipFixFlash"],
        "录像": ["videotapeCanAccelerate"],
        "头像": ["cantChangeHeadPortrait"]
    }
    intent_dict = {}
    for _ in entities:
        intents = entity_intent_dict.get(_, [])
        for _ in intents:
            if intent_dict.get(_, 0) == 0:
                intent_dict[_] = 1
            else:
                intent_dict[_] = intent_dict.get(_) + 1
    intent_ranking = sorted(intent_dict.items(), key=lambda x: x[1], reverse=True)
    intent_rank_name = [_[0] for _ in intent_ranking[:6]]
    return intent_rank_name


if __name__ == '__main__':
    entity_compile_intent(["平板", "课堂", "声音"])
