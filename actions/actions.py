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


class ActionDispatchPatronesArq(Action):
    def name(self) -> Text:
        return "action_dispatch_patrones_arq"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_entity_value = tracker.latest_message['entities'][0]['value']
        print(tracker.latest_message['entities'][0])

        if last_entity_value == 'capas':
            dispatcher.utter_message(response="utter_pregunta_patrones/capas")
        elif last_entity_value == 'cliente-servidor':
            dispatcher.utter_message(response="utter_pregunta_patrones/cliente-servidor")
        elif last_entity_value == 'maestro-esclavo':
            dispatcher.utter_message(response="utter_pregunta_patrones/maestro-esclavo")
        elif last_entity_value == 'pipe-filter':
            dispatcher.utter_message(response="utter_pregunta_patrones/pipe-filter")
        elif last_entity_value == 'broker':
            dispatcher.utter_message(response="utter_pregunta_patrones/broker")
        elif last_entity_value == 'peer-to-peer':
            dispatcher.utter_message(response="utter_pregunta_patrones/peer-to-peer")
        elif last_entity_value == 'event-bus':
            dispatcher.utter_message(response="utter_pregunta_patrones/event-bus")
        elif last_entity_value == 'mvc':
            dispatcher.utter_message(response="utter_pregunta_patrones/mvc")
        elif last_entity_value == 'blackboard':
            dispatcher.utter_message(response="utter_pregunta_patrones/blackboard")
        elif last_entity_value == 'interpreter':
            dispatcher.utter_message(response="utter_pregunta_patrones/interpreter")
        else:
            print('bueno no se que queres saber flaco')

        return []

class ActionDispatchPatronesPoo(Action):
    def name(self) -> Text:
        return "action_dispatch_patrones_poo"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_entity_value = tracker.latest_message['entities'][0]['value']
        print(tracker.latest_message['entities'][0])

        if last_entity_value == 'abstract factory':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/abstract-factory")
        elif last_entity_value == 'factory method':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/factory-method")
        elif last_entity_value == 'builder':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/builder")
        elif last_entity_value == 'prototype':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/prototype")
        elif last_entity_value == 'singleton':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/singleton")
        elif last_entity_value == 'adapter':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/adapter")
        elif last_entity_value == 'bridge':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/bridge")
        elif last_entity_value == 'composite':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/composite")
        elif last_entity_value == 'decorator':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/decorator")
        elif last_entity_value == 'facade':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/facade")
        elif last_entity_value == 'flyweight':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/flyweight")
        elif last_entity_value == 'proxy':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/proxy")
        elif last_entity_value == 'chain of responsibility':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/chain-of-responsibility")
        elif last_entity_value == 'command':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/command")
        elif last_entity_value == 'memento':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/memento")
        elif last_entity_value == 'iterator':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/iterator")
        elif last_entity_value == 'mediator':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/mediator")
        elif last_entity_value == 'observer':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/observer")
        elif last_entity_value == 'state':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/state")
        elif last_entity_value == 'strategy':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/strategy")
        elif last_entity_value == 'template method':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/template-method")
        elif last_entity_value == 'visitor':
            dispatcher.utter_message(response="utter_pregunta_patrones_poo/visitor")
        else:
            print('bueno no se que queres saber flaco')

        return []

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
