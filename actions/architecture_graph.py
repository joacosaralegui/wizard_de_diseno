import pygraphviz as pgv
import enchant 
import os 
from rasa_sdk.events import SlotSet
from datetime import datetime
from .mongo_client import load_arqui, save_arqui

class GraphManager:
    def __init__(self, id):
        self.id = id
        # Fetch graph or create
        graph = load_arqui(id)
        if graph:
            self.graph = pgv.AGraph(string=graph['arqui'])
        else:
            self.graph = self.create_new()

    def create_new(self):
        return pgv.AGraph(strict=False,directed=True)

    def save(self):
        return save_arqui(self.id, self.graph.to_string())

    def update_graph_with_new_entities(self,entities,intent):
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
        filename = 'actions/images/file'+ str(datetime.now()) +'.png'
        self.draw_in_file(filename)
        return filename

    def draw_in_file(self,filename):
        self.graph.layout(prog='dot') 
        self.graph.draw(filename) 

    def add_node(self,node):
        self.graph.add_node(node.name,color=node.get_color(),shape=node.get_shape())

    def update_name_if_similar_found_in_graph(self,node_to_add):
        closest = {'node':None,'distance':3}
        for node_to_compare in self.graph.nodes():
            calculated_distance = enchant.utils.levenshtein(node_to_compare, node_to_add.name)
            if calculated_distance < closest['distance']:
                closest['node'], closest['distance']= node_to_compare, calculated_distance
        
        if closest['node'] != None:
            node_to_add.name = closest['node'].name

    def get_closest_node(self,reference_node,nodes):
        prev_node = nodes[0]
        if reference_node.start < prev_node.start:
            return prev_node
        else:
            for node in nodes[1:]:
                if reference_node.end < node.start:
                    if abs(reference_node.start - prev_node.end) <  abs(reference_node.end - node.start):
                        return prev_node
                    else:
                        return node
                else:
                    prev_node = node
            return prev_node

    def enough_nodes(self,nodes):
        return len(nodes) >= 2

    def update_edge_label(self,edge,entity):
        label = edge.attr['label']
        if entity.name not in label:
            edge.attr['label'] += ", " + entity.name

    def add_labeled_edge(self,node1,node2,entity):
        if self.graph.has_edge(node1.name,node2.name):
            edge = self.graph.get_edge(node1.name, node2.name) 
            self.update_edge_label(edge,entity)
        else:
            self.graph.add_edge(node1.name, node2.name, label=entity.name)  

    def add_edge(self,node1,node2):
        self.graph.add_edge(node1.name, node2.name)  

    def find_nodes_connected_by_event(self,event,nodes):     
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
        for node in nodes:
            self.update_name_if_similar_found_in_graph(node)
            self.add_node(node)

    def update_events(self,nodes,entities):
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

