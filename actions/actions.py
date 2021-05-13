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
        
        last_entity_value = tracker.latest_message['entities'][0]['value']
        print(tracker.latest_message['entities'][0])

        if last_entity_value == 'patron':
            dispatcher.utter_message(response="utter_concepto_patron")
        elif last_entity_value == 'Scrum' or last_entity_value == 'scrum': # Aca habria un elif para cada set de conceptos/sinonimos
            dispatcher.utter_message(response="utter_concepto_scrum")
        elif last_entity_value == 'agil':
            dispatcher.utter_message(response="utter_concepto_agil")
        elif last_entity_value == 'FDD':
            dispatcher.utter_message(response="utter_concepto_FDD")
        elif last_entity_value == 'template':
            dispatcher.utter_message(response="utter_concepto_template")
        elif last_entity_value == 'atributo-de-calidad':
            dispatcher.utter_message(response="utter_concepto_atributo-de-calidad")
        elif last_entity_value == 'hook':
            dispatcher.utter_message(response="utter_concepto_hook")
        elif last_entity_value == 'requerimiento-funcional':
            dispatcher.utter_message(response="utter_concepto_FDD")
        elif last_entity_value == 'requerimiento-no-funcional':
            dispatcher.utter_message(response="utter_concepto_requerimiento-no-funcional")
        else:
            print('bueno no se que queres saber flaco')

        return []
