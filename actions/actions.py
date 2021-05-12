# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionExplainConcept(Action):

     def name(self) -> Text:
         return "action_explain_concept"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        patron_set = {"patron", "patrón", "Patrón", "pattern", "patron de diseño", "design pattern"}
        scrum_set = {"Scrum", "scrum", "Metodología Scrum"}
        print(patron_set)
        
        last_entity_value = tracker.latest_message['entities'][0]['value']

        if last_entity_value in patron_set:
            dispatcher.utter_message(response="utter_concepto_patron")
        elif last_entity_value in scrum_set: # Aca habria un elif para cada set de conceptos/sinonimos
            dispatcher.utter_message(response="utter_concepto_scrum")

        return []
