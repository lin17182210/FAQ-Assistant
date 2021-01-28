#!/usr/bin/python
# -*- coding:utf-8 -*-
from typing import Text, List
import requests
import pymysql
import logging

logger = logging.getLogger(__name__)
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


def retrieval_intent(intent: Text) -> Text:
    default_intent_response = {
        "更新了备课模块是否会同步至课表": "您好，备课模块更新不会同步到课表，需要进行重新关联，课表备课更新会同步到备课模块的备课包中。",
        "点播课章节无法完成": "您好，单纯的PPT课件，不符合完成的条件。您阅读完成即可",
        "没有权限查看考试": "您好，查看需要绑定对应的学科学段和班级，需要在网页端进行修改和绑定班级。",
        "课堂中出现乱码": "您好，这个由于是浏览器的极速模式导致的，可以在网址栏的最后点击闪电标志切换到兼容模式或者换个浏览器尝试。",
        "学生上课听不到老师的声音": "您好，如果是个别学生，麻烦让学生在个人中心里切换下平板设置里面的“课堂线路”或者暂时换个网络环境；如果是大多数，您先更换下网络环境。",
        "如何锁定屏幕": "您好，默认的锁屏需要在首页点击“头像”-“设置”-“课堂设置”中进行设置。课中的临时锁屏点击左上角头像-“课堂设置”-“锁屏”。",
        "如何变声": "您好，在课中点击左上角头像-“课堂设置”-“变声”，先完成录音，在弹出的变声弹窗中调节音色",
        "给学生授权后，课件是否可以翻页": "您好，课中没有授权的情况下可以开启和关闭课件的自由翻页功能，授权的情况下无法进行自由翻页。",
        "试卷讲评没有相关的考试": "您好，需要满足2个条件：您的课是行政班或是学考班的课程，且考试已经公布了成绩。",
        "移动讨论区": "您好，双击讨论区蓝色边框可进行上浮移动。讨论区和课件是否重叠跟电脑自身分辨率有关，不影响学生观看课件。",
        "平板上课件加载不出来": "您好，平板上课件加载不出，很可能是网络不稳定导致的。建议切换信号较好的WiFi尝试下，同时注意下系统时间是否正常，如果出现时间异常也可能导致加载不出，需要您校准系统时间。",
        "平板进入课堂的按钮消失": "您好，可能是平板页面排版问题，点击平板“设置”—“显示”—“字体大小”，进行字体调节。",
        "如何排临时课表": "您好，平板端在线校园课堂——临时课表，点击右下角“我要排课”小图标进行临时排课。PC端的功能按钮位于：“在线校园课堂”——“临时课表”。点击右上角“我要排课”小图标进行临时排课。",
        "平板无法进入课堂": "您好，平板无法进入课堂可能是网络问题导致的。建议您尝试点击头像--切换课堂线路，或者切换信号较好的WiFi。",
        "如何外放学生的声音": "您好，我们的平板为了保证上课时的安静，默认关闭学生平板声音外放，如果需要学生平板声音外放。只要点击左侧头像——允许学生平板外放声音即可。",
        "连麦没有声音": "您好，您先使用QQ语音和朋友打电话，检测是不是电脑的问题；如果通话正常，这边技术人员帮您远程调试",
        "学生考试后没有成绩": "您好，学生考试之后是否手动点击提交试卷。如果没有，是否在考试后点击补交试卷，如果没有，那么确实是没有分数的。如果手动提交了试卷或者考试后补交，请提供账号密码，这边帮您进一步解决。",
        "平板是否可以编辑资源": "您好，平板无法编辑题目，可去网页端进行编辑。",
        "微课无法上传": "您好，课中上传的微课大小不得大于50M。您可以通过资源库或者备课包进行上传。",
        "上传课件后在我的资源里找不到": "这种情况一般为账号绑定了多个学科学段，在我的资源里，“+”号右边的按钮可以切换学段学科。选择你所绑定的其他学科即可。",
        "微课录制出现闪退": "先进入平板设置——存储，查看当前平板的存储空间是否足够。进入乐课APP首页，点击设置——异常上报。",
        "修改作业选择的学生": "您好，这可能是您的班级成员名单有改动导致的。您在之后的作业模块布置作业时，不要点击“最近常用”，重新选择一下学生和班级，数据会自动同步更新的。",
        "取消作业": "您好，在作业模块，找到这份作业，点击“更多操作”，“作废”。",
        "如何布置拍照作业": "您好，布置作业时，在“试卷批改方式”一栏将“按分数批改”切换为“按对错批改”。拍照作业为对错作业，在“按分数批改”的模式下是无法选中的",
        "修改作业的时间": "您好，在作业模块找到指定作业，点击“更多操作”-“修改时间”。在作业开始时间之前，可以修改开始时间和截止时间；在作业开始之后，只可以修改截止时间；在截止时间之后，就不能修改了。",
        "作业类型": "您好，备课包中布置的三合一作业(课前的预习、课中的随堂测试、课后的复习)以及作业模块中布置的拍照作业属于对错作业；作业模块布置的普通作业同时具备设置为对错作业和分数作业的功能。",
        "平板如何打出音标": "您好，长按字母，会出现音标提示，选择即可。",
        "修复flash": "您好，可以进入浏览器设置，将缓存清理掉，再重新修复下flash试试。",
        "录像是否可以倍速播放": "您好，目前暂时还不支持录像倍速播放，该功能还在完善中。",
        "无法修改头像": "您好，学校设置了更换头像的次数，更换头像是有限的。",
    }
    
    return default_intent_response.get(intent, None)


def get_record_db_cursor():
    try:
        db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="python",
            db="rasa",
            charset="utf8"
        )
        db.cursor().close()
    except Exception as e:
        logger.error(e)
    else:
        return db.cursor()
    

if __name__ == '__main__':
    retrieval_intent(None)
