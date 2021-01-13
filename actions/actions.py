# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, Any, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from actions.utils import fetch


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
        return []
