from rasa.nlu.model import Interpreter
from .entities import Entity
from .architecture_graph import GraphManager
import os
# path of your model
rasa_model_path = "actions/models/modelado/nlu"

# create an interpreter object
interpreter = Interpreter.load(rasa_model_path)

def rasa_output(text):
    """
    Analisis NLU del texto para clasificar categorias de patrones:
    usa modelo de -> (https://github.com/joacosaralegui/analisis-de-patrones)
    """
    message = str(text).strip()
    result = interpreter.parse(message)
    return result

def update_graph(id,text):
    # Get analisis
    rasa_parsing = rasa_output(text)
    intent = rasa_parsing['intent']['name']
    entities = parse_entities(rasa_parsing['entities'])
    print_summary(entities)

    # Update graph
    graph_manager = GraphManager(id)
    graph_manager.update_graph_with_new_entities(entities,intent)
    graph_manager.save()

    # Image
    graph_image_file = graph_manager.get_image_file()
    return "Qué te parece esto?",os.path.abspath(graph_image_file)

#
# Helper functions  
#
def parse_entities(entities_list): 
    entities = [Entity(e) for e in entities_list]
    return get_valid_entities(entities)

def get_valid_entities(entities):
    return [e for e in entities if e.is_valid()]
    
def print_summary(entities):
    print("***  New requirement  ****")
    print("Entities: ")
    for e in entities:
        print(f" - {e.category}: {e.name}")
    print("*************************")
