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


# class ActionWeatherForm(FormAction):
#
#     def name(self) -> Text:
#         return "weather_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["address", "date_time"]
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         address = tracker.get_slot('address')
#         date_time = tracker.get_slot('date_time')
#         try:
#             weather_data = fetch(address, date_time)
#         except Exception as e:
#             weather_data = "{}".format(e)
#         dispatcher.utter_message(weather_data)
#         return [AllSlotsReset()]

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
        return [AllSlotsReset()]


class ActionFallBack(Action):
    
    def name(self) -> Text:
        return "action_fallback"
    
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        AllSlotsReset()
        entities = tracker.latest_message.get("entities", [])
        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        highest_ranking_intent = intent_ranking[1]
        if highest_ranking_intent.get("confidence") <= 0.3:
            entity_confidence_list = [(_.get("value"), _.get("confidence")) for _ in entities]
            sorted_entities = sorted(entity_confidence_list, key=lambda x: x[1], reverse=True)[:5]
            entity_list = [_[0] for _ in sorted_entities]
            if len(entity_list) > 0:
                text = ",".join(entity_list)
                dispatcher.utter_message(text=f"检测到输入的实体: {text}")
            else:
                dispatcher.utter_message(template="utter_default")
                dispatcher.utter_message(md("您可以这样向我提问: "
                                            "<br/>1.给学生授权后能进行课件翻页吗<br/>\
                                            2.无法移动讨论区<br/>\
                                            3.如何排临时课表<br/>\
                                            4.直播上课连麦没有声音<br/>\
                                            5.如何进行锁屏<br/>\
                                            6.学生按时考试但是没有成绩<br/>\
                                            7.为什么我的试卷讲评没有相关考试"))
        else:
            # 获取意图 description
            button_list = []
            for intent in intent_ranking[1:6]:
                button_list.append({"title": intent.get("confidence", 0), "payload": intent.get("name", None)})
            dispatcher.utter_message(text="你可能是想询问：")
            dispatcher.utter_message(buttons=button_list)
        # slots = current_state.get("slots")
        # button_list = []
        # for k, v in slots.items():
        #     if v is not None:
        #         button_list.append({"title": k, "payload": v})
        # if len(button_list) > 0:
        #     dispatcher.utter_message(text="逐步确认信息....")
        #     dispatcher.utter_message(buttons=button_list)
        # else:
        #     dispatcher.utter_message(md("您可以这样向我提问: "
        #                                 "<br/>1.给学生授权后能进行课件翻页吗<br/>\
        #                                 2.无法移动讨论区<br/>\
        #                                 3.如何排临时课表<br/>\
        #                                 4.直播上课连麦没有声音<br/>\
        #                                 5.如何进行锁屏<br/>\
        #                                 6.学生按时考试但是没有成绩<br/>\
        #                                 7.为什么我的试卷讲评没有相关考试"))
        return [AllSlotsReset()]
