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
            summary = "La verdad que no sé... porqué no hablamos de otra cosa?"
        dispatcher.utter_message(summary)
        
        return [FollowupAction("action_listen")]

class ActionModelado(Action):

    def name(self) -> Text:
        return "action_modelado"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:

        text =  tracker.latest_message['text']
        utter, image = update_graph(tracker.sender_id, text)
        dispatcher.utter_message(text=utter)
        dispatcher.utter_message(image=image)
        return[]