import pygraphviz as pgv
import enchant 
import os 
from rasa_sdk.events import SlotSet
from datetime import datetime
from .mongo_client import load_arqui, save_arqui,remove_arqui

class GraphManager:
    """
    Esta clase administra los grafos que modelan las arquitecturas y se encarga
    de generarlos, actualizarlos y eliminarlos
    Almacena una serie de grafos para un ID particular, que puede ser ID de usuario, 
    proyecto o cualquier otro contexto
    El tiempo de vida del manager es dentro de una unica custom action que busca
    hacer 1 actualizacion a partir de un unico requerimiento o elimiar algo
    No soporta multiples acciones a la vez
    """
    
    def __init__(self, id):
        """
        Inicializa el Manager. 
        Carga el id del usuario y su grafo de arqui si lo tiene asociado
        Si no lo tiene, crea un grafo nuevo.
        """
        self.id = id

        graph = load_arqui(id)
        if graph:
            self.graph = pgv.AGraph(string=graph['arqui'])
        else:
            self.graph = self.create_new()

    def create_new(self):
        """
        Crear grafo nuevo
        """
        return pgv.AGraph(strict=False,directed=True)

    def save(self):
        """
        Almacenar nueva version de la arqui en mongodb
        """
        return save_arqui(self.id, self.graph.to_string())

    def remove_last(self):
        # TODO: eliminar grafo
        return

    def update_graph_with_new_entities(self,entities,intent):
        """
        De acuerdo a la estructura clasificada en el intent,
        cargamos las entidades de una manera específica 
        en el grafo
        """
        # TODO: hacer un refactor de esta funcion, es un asquito
        print(intent)
        if intent == "star":
            self.update_graph_with_star_entities(entities)
        elif intent == "simple_chain" or intent == "double_chain":
            self.update_graph_with_chained_entities(entities)  
        elif intent == "star_and_double_chain":
            cut_index = len(entities)-2

            if len(entities) > cut_index + 1:
                self.update_graph_with_star_entities(entities[:cut_index+1])
                self.update_graph_with_chained_entities(entities[cut_index:])  
        elif intent == "star_and_simple_chain":
            cut_index = len(entities)-1

            if len(entities) > cut_index:
                self.update_graph_with_star_entities(entities[:cut_index+1])
                self.update_graph_with_chained_entities(entities[cut_index:])  
        else:
            nodes = [e for e in entities if e.is_node()]
            if "simple" in intent and len(nodes) > 1:
                cut_index = entities.index(nodes[1])
            elif "double" in intent  and len(nodes) > 2:
                cut_index = entities.index(nodes[2])
            else: 
                cut_index = len(entities)-1

            if len(entities) > cut_index:
                self.update_graph_with_chained_entities(entities[:cut_index+1])
                self.update_graph_with_star_entities(entities[cut_index:])  


    def get_image_file(self):
        """
        Genera una imagen para representar el estado actual de la arquitectura
        """
        filename = 'actions/images/file'+ str(datetime.now()) +'.png'
        self.graph.layout(prog='dot') 
        self.graph.draw(filename) 
        return filename


    def add_node(self,node):
        """
        Agregar nodo al grafo
        """
        self.graph.add_node(node.name,color=node.get_color(),shape=node.get_shape())

    def update_name_if_similar_found_in_graph(self,node_to_add):
        """
        Si encontramos en el grafo un nodo con nombre similar al que queremos agregar, 
        le cambiamos el nombre al nodo a agregar para que sea el mismo del que ya esta
        """
        # TODO: si alguno incluye a otro entonces tmb los podriamos tomar como iguales
        closest = {'node':None,'distance':3}
        for node_to_compare in self.graph.nodes():
            calculated_distance = enchant.utils.levenshtein(node_to_compare, node_to_add.name)
            if calculated_distance < closest['distance']:
                closest['node'], closest['distance']= node_to_compare, calculated_distance
        
        if closest['node'] != None:
            node_to_add.name = closest['node'].name

    def get_closest_node(self,ref_entity,node_entities):
        """
        Dado una entidad de referencia buscar la entidad nodo mas cercana
        de acuerdo a la posicion en el texto del requerimiento
        Esta función busca asignar propiedades al nodo mas cercano en distancia  del texto del req
        """
        prev_node = node_entities[0]
        if ref_entity.start < prev_node.start:
            return prev_node
        else:
            for node in node_entities[1:]:
                if ref_entity.end < node.start:
                    if abs(ref_entity.start - prev_node.end) <  abs(ref_entity.end - node.start):
                        return prev_node
                    else:
                        return node
                else:
                    prev_node = node
            return prev_node

    def enough_nodes(self,nodes):
        """
        Chequeo si tengo al menos dos nodos,sino no puedo armar nada en el grafo 
        """
        return len(nodes) > 1

    def update_edge_label(self,edge,entity):
        """
        actualizar un label de arista con el nombre de una entidad
        Si ya tiene una, agregar la nueva
        """
        label = edge.attr['label']
        if entity.name not in label:
            edge.attr['label'] += ", " + entity.name

    def add_labeled_edge(self,node1,node2,entity):
        """
        Agregar una arista entre dos nodos. 
        Si la arista ya existe, simplemente actualizar la etiqueta
        """
        if self.graph.has_edge(node1.name,node2.name):
            edge = self.graph.get_edge(node1.name, node2.name) 
            self.update_edge_label(edge,entity)
        else:
            self.graph.add_edge(node1.name, node2.name, label=entity.name)  

    def add_edge(self,node1,node2):
        """
        Agregar arista sin etiqueta entre dos nodos
        """
        if not self.graph.has_edge(node1.name,node2.name):
            self.graph.add_edge(node1.name, node2.name)  

    def find_nodes_connected_by_event(self,event,nodes):   
        """
        Dado un evento, definir que dos nodos/entidades conecta
        Se hace en relacion a la posicion de las entidades en el texto
        """  
        i = 0
        first_node,second_node = nodes[i],nodes[i+1]
        while i < len(nodes)-2:
            if event.end < second_node.start:
                return first_node, second_node
            else:
                i += 1
                first_node,second_node = nodes[i],nodes[i+1]
        return first_node,second_node           

    def update_nodes(self,nodes):
        """
        Agrega nodos pero primero actualizar los nombres si ya estan en el grafo
        """
        for node in nodes:
            self.update_name_if_similar_found_in_graph(node)
            self.add_node(node)

    def update_events(self,nodes,entities):
        """
        Para los nodos 
        """
        events = [e for e in entities if e.is_event()]
        for event in events:
            node1,node2 = self.find_nodes_connected_by_event(event,nodes)          
            self.add_labeled_edge(node1,node2,event)
    
    def update_properties(self,nodes,entities):
        properties = [e for e in entities if e.is_property()]
        for property_node in properties:
            if property_node not in nodes:
                closest_node = self.get_closest_node(property_node,nodes)
                self.add_node(property_node)
                self.add_edge(closest_node, property_node)  

    def connect_unconnected_nodes(self,nodes):
        prev_node = nodes[0]
        for node in nodes[1:]:
            if not self.graph.has_edge(prev_node.name,node.name):
                self.add_edge(prev_node,node)
                self.add_edge(node,prev_node)
            prev_node = node

    def update_graph_with_chained_entities(self,entities):
        nodes = [e for e in entities if e.is_node()]
        if not self.enough_nodes(nodes):
            nodes = [e for e in entities if e.is_node() or e.is_property()]
        if not self.enough_nodes(nodes):
            return

        self.update_nodes(nodes)
        self.update_events(nodes,entities)
        self.update_properties(nodes,entities)
        self.connect_unconnected_nodes(nodes)


    def update_graph_with_star_entities(self,entities):
        nodes = [e for e in entities if e.is_node()]
        if not self.enough_nodes(nodes):
            nodes = [e for e in entities if e.is_node() or e.is_property()]
        
        if not self.enough_nodes(nodes):
            return
        
        self.update_nodes(nodes)
        self.update_properties(nodes,entities)
        
        main_node = nodes[0]
        for idx, entity in enumerate(entities[:-1]):
            next_entity = entities[idx+1]
            if entity.is_event() and next_entity.is_node() or next_entity.is_property() and next_entity != main_node:
                self.add_labeled_edge(main_node,next_entity,entity)

        for node in nodes[1:]:
            if not self.graph.has_edge(main_node.name,node.name):
                self.add_edge(main_node,node)

