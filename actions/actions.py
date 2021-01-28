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
from actions.utils import fetch_intent_description, entity_compile_intent, retrieval_intent
from markdownify import markdownify as md
import logging


logger = logging.getLogger(__name__)


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
        latest_message = tracker.latest_message.get("text")
        default_response = retrieval_intent(latest_message)
        if default_response:
            logger.debug("return default response")
            dispatcher.utter_message(text=default_response)
        elif not latest_message:
            logger.debug("user don't input message")
            self.default_dispatcher(dispatcher)
        else:
            entities = tracker.latest_message.get("entities", [])
            intent_ranking = tracker.latest_message.get("intent_ranking", [])
            highest_ranking_intent = intent_ranking[1]
            entity_confidence_list = [(_.get("value"), _.get("confidence")) for _ in entities]
            if len(entity_confidence_list) == 0:
                logger.debug("message don't contain entities")
                self.default_dispatcher(dispatcher)
            else:
                if highest_ranking_intent.get("confidence") <= 0.3:
                    logger.debug(f"retrieval intent by entities...{entities}")
                    entity_list = [_.get("value") for _ in entities]
                    if entity_list:
                        # 根据实体检索意图
                        intent_rank_name = entity_compile_intent(entity_list)
                        self.get_button_list(dispatcher, intent_rank_name)
                    else:
                        self.default_dispatcher(dispatcher)
                else:
                    # 获取意图 预定义 description
                    logger.debug(f"return possible top-5 intent....{intent_ranking}")
                    intent_rank_name = [_.get("name") for _ in intent_ranking[1:10] if _.get("confidence") >= 0.15]
                    self.get_button_list(dispatcher, intent_rank_name)
        return [AllSlotsReset()]
    
    @staticmethod
    def get_button_list(dispatcher, intent_rank_name: List[Text]) -> None:
        intent_desc_list = fetch_intent_description(intent_rank_name)
        button_list = []
        for index, intent in enumerate(intent_desc_list):
            button_list.append({"title": index + 1, "payload": intent})
        dispatcher.utter_message(text="你可能是想询问：")
        dispatcher.utter_message(buttons=button_list)
    
    @staticmethod
    def default_dispatcher(dispatcher):
        dispatcher.utter_message(template="utter_default")
        dispatcher.utter_message(md("您可以这样向我提问: "
                                    "<br/>1.给学生授权后能进行课件翻页吗<br/>\
                                    2.无法移动讨论区<br/>\
                                    3.如何排临时课表<br/>\
                                    4.直播上课连麦没有声音<br/>\
                                    5.如何进行锁屏<br/>\
                                    6.学生按时考试但是没有成绩<br/>\
                                    7.为什么我的试卷讲评没有相关考试"))