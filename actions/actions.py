# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Text, Any, Dict, List
from rasa_sdk import Tracker, Action
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from actions.utils import fetch
from markdownify import markdownify as md


class ActionWeatherForm(FormAction):

    def name(self) -> Text:
        return "weather_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["address", "date_time"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date_time')
        try:
            weather_data = fetch(address, date_time)
        except Exception as e:
            weather_data = "{}".format(e)
        dispatcher.utter_message(weather_data)
        return [AllSlotsReset()]


class ActionFirst(Action):
    
    def name(self) -> Text:
        return "action_first"
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        dispatcher.utter_message(template="utter_whoareyou")
        dispatcher.utter_message(md("您可以这样向我提问: "
                                    "<br/>1.给学生授权后能进行课件翻页吗<br/>\
                                    2.无法移动讨论区<br/>\
                                    3.如何排临时课表<br/>\
                                    4.直播上课连麦没有声音<br/>\
                                    5.如何进行锁屏<br/>\
                                    6.学生按时考试但是没有成绩<br/>\
                                    7.为什么我的试卷讲评没有相关考试"))
        return []


class ActionFallBack(Action):
    
    def name(self) -> Text:
        return "action_fallback"
    
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_default")
        dispatcher.utter_message(md("您可以这样向我提问: "
                                    "<br/>1.给学生授权后能进行课件翻页吗<br/>\
                                    2.无法移动讨论区<br/>\
                                    3.如何排临时课表<br/>\
                                    4.直播上课连麦没有声音<br/>\
                                    5.如何进行锁屏<br/>\
                                    6.学生按时考试但是没有成绩<br/>\
                                    7.为什么我的试卷讲评没有相关考试"))
        return []
