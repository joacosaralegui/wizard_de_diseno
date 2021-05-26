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


class ActionDispatchPatrones(Action):
    def name(self) -> Text:
        return "action_dispatch_patrones"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.get_intent_of_latest_message()
        last_entity_value = tracker.latest_message['entities'][0]['value']

        utter = 'utter_'+ last_intent + '/' + last_entity_value

        dispatcher.utter_message(response=utter)

        return []

class ActionEjemplo(Action):
    def name(self) -> Text:
        return "action_ejemplo"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        utter = get_latest_questions(tracker.events)[0]
        
        #intento retornar con el utter que no se si existe
        try:
            retorno = FollowupAction(name='utter_' + utter + '_ejemplo')
            return[retorno]
        except:
            # si dio error busco en wiki
            try:
                text = tracker.latest_message['text']
                print('texto a buscar en wiki: ' + text) # ver como buscar mensje anterior a este
                summary = wikipedia.summary(text, sentences=1)
            except:
                # si no funco wiki tampoco
                summary = "La verdad que no entiendo que es lo que queres... " 
                dispatcher.utter_message(summary)
                FollowupAction("action_listen")
        return []

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
