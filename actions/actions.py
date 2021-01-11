# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
from typing import Text, Any, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from .utils import fetch_weather


class ActionWeatherForm(FormAction):

    def name(self) -> Text:
        return "weather_form"
    
    @staticmethod
    async def required_slots(tracker: Tracker) -> List[Text]:
        return ["address"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        address = tracker.get_slot('address')
        weather_data = fetch_weather(address)
        dispatcher.utter_message(weather_data)
        return []
