# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

import wikipedia
from wikipedia.wikipedia import summary
wikipedia.set_lang("es")

def get_latest_questions(events):
    # Extrae los ultimos intents que tengan "pregunta_" en el nombre
    return [e['parse_data']['response_selector']['default']['response']['intent_response_key'] for e in events if e['event'] == 'user' and 'pregunta_' in e['parse_data']['intent']['name']]

class ActionClarification(Action):
    def name(self) -> Text:
        return "action_clarificacion"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        utter = get_latest_questions(tracker.events)[0]
        # pregunta_concepto/patron
        # utter_pregunta_concepto/patron_clarificacion

        # TODO: soportar cuando vuelve a no entender (1 nivel de recursividad de no entender)
        # SI tiene clarificacion -> no me rompas las bolas
        # TODO: chequear que exista y sino decir que -> nom me rompas als bolas

        return [FollowupAction(name='utter_' + utter + '_clarificacion')]


class ActionEjemplo(Action):
    def name(self) -> Text:
        return "action_ejempĺo"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        utter = get_latest_questions(tracker.events)[0]
        # pregunta_concepto/patron
        # utter_pregunta_concepto/patron_clarificacion

        # TODO: soportar cuando vuelve a no entender (1 nivel de recursividad de no entender)
        # SI tiene clarificacion -> no me rompas las bolas
        # TODO: chequear que exista y sino decir que -> nom me rompas als bolas

        return [FollowupAction(name='utter_' + utter + '_ejemplo')]

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:
    
        text = tracker.latest_message['text']

        try:
            summary = wikipedia.summary(text, sentences=1)
        except:
            # TODO: add otras opciones!! (UTTER??)
            summary = "Que pregunta más básica. No tenes algo mejor?"
        dispatcher.utter_message(summary)
        FollowupAction("action_listen")

        # Revert user message which led to fallback.
        return []

class ActionExplainConcept(Action):

    def name(self) -> Text:
        return "action_explain_concept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
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
        """
        return []
