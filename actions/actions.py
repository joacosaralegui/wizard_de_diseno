# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from rasa_sdk.forms import FormValidationAction

from .analisis_de_patrones import get_recomendacion
from .modelado import update_graph

# Setup wikipedia
import wikipedia
wikipedia.set_lang("es")

# Extrae los ultimos intents que tengan "pregunta_" en el nombre
def get_ultimos_utter_pregunta(events):
    return [e['metadata']['utter_action'] for e in events if e['event'] == 'bot' and 'utter_action' in e['metadata'] and 'pregunta_' in e['metadata']['utter_action']]

class ActionClarification(Action):
    """Esta funcion se encarga de buscar un utter de clarificacion en base al intent detectado, 
    se acciona con el intent de no_entendio"""
    def name(self) -> Text:
        return "action_clarificacion"    # con intent no entendio... 

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ultimos_utter = get_ultimos_utter_pregunta(tracker.events)
        
        if ultimos_utter:
            ultimo_utter = ultimos_utter[0]
            accion_a_responder = 'utter_' + ultimo_utter + '_clarificacion'
            print('action de clarificacion a buscar: ' + accion_a_responder)
            
            lista_acciones = domain['responses']
            if accion_a_responder in lista_acciones:
                dispatcher.utter_message(response=accion_a_responder)
            else:
                dispatcher.utter_message(text='Ya lo deje muy claro, no se me ocurre otra manera...')
        else:
            dispatcher.utter_message(text="No hay nada que entender. Haceme alguna pregunta interesante")
        
        return []

class ActionDispatchPatrones(Action):
    """Esta funcion se dispara cada vez que alguien pide una pregunta de patrones.
    Devuelve un utter con la respuesta para ese patron en particular"""
    def name(self) -> Text:
        return "action_dispatch_patrones"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ultimo_intent = tracker.get_intent_of_latest_message()
        try:
            ultima_entidad = tracker.latest_message['entities'][0]['value']
        except: 
            dispatcher.utter_message(text='Es una buena pregunta, la verdad que no tengo idea.')
            return []
        utter_a_responder = 'utter_'+ ultimo_intent + '/' + ultima_entidad
        
        lista_acciones = domain['responses']
        if utter_a_responder in lista_acciones:
            dispatcher.utter_message(response=utter_a_responder)
        else:
            dispatcher.utter_message(text='Es una buena pregunta, la verdad que no tengo idea. Preguntame alguna otra cosa, la segunda es la vencida.')
    
        return []

class ActionEjemplo(Action):
    """Esta funcion se encarga de buscar una utter de ejemplo en base al intent detectado,
    se acciona con el intent de ejemplo"""
    def name(self) -> Text:
        return "action_ejemplo"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        ultimos_utter = get_ultimos_utter_pregunta(tracker.events)
        
        if ultimos_utter:
            ultimo_utter = ultimos_utter[0]
            accion_a_responder = 'utter_' + ultimo_utter + '_ejemplo'
            print('action de ejemplo a buscar: ' + accion_a_responder)
            
            lista_acciones = domain['responses']
            if accion_a_responder in lista_acciones:
                dispatcher.utter_message(response=accion_a_responder)
            else:
                dispatcher.utter_message(text='No tengo ejemplos de eso...')
        else:
            dispatcher.utter_message(text="Ejemplos de qu??? Est??s bien vos? Preguntame algo en serio..")
        
        return []

class ActionDefaultFallback(Action):
    """Ejecuta una accion de fallback que busca en wikipedia lo que no entiende el bot"""

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
            summary = "La verdad que no s??... porqu?? no hablamos de otra cosa?"
        dispatcher.utter_message(summary)
        
        return [FollowupAction("action_listen")]

class ActionSugerenciaPatron(Action):

    def name(self) -> Text:
        return "action_sugerencia_patron"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:

        text = tracker.get_slot('problema')
        utter = get_recomendacion(text)
        dispatcher.utter_message(text=utter)
        return[]


class ActionExplicacionPatron(Action):
    def name(self) -> Text:
        return "action_explicacion_patron"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_pregunta_concepto/patron")

class ActionModelado(Action):

    def name(self) -> Text:
        return "action_modelado"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:

        text = tracker.get_slot('requerimiento')
        utter, image = update_graph(tracker.sender_id, text)
        dispatcher.utter_message(text=utter)
        dispatcher.utter_message(image=image)
        return[]