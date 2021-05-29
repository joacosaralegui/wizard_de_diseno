SYSTEM = "Sistema"

class Entity:
    colors = {"MODEL":"blue","SYSTEM":"red","PROVIDER":"yellow","PROPERTY":"cyan"}
    shapes = {"MODEL":"box","SYSTEM":"oval","PROVIDER":"box","PROPERTY":"house"}

    def __init__(self, entity_object):
        self.category = entity_object['entity']
        self.name = entity_object['value']
        self.confidence = entity_object['confidence_entity']
        self.start = entity_object['start']
        self.end = entity_object['end']

        if self.matches_category("SYSTEM"):
            self.name = SYSTEM

    def matches_category(self,category):
        return self.category == category

    def is_node(self):
        return not self.is_event() and not self.is_property()

    def is_event(self):
        return self.matches_category("EVENT")
    
    def is_property(self):
        return self.matches_category("PROPERTY")

    def is_valid(self):
        return self.is_long_enough() and self.is_confidence_enough()

    def is_long_enough(self,min_length_required=2):
        return len(self.name) > min_length_required

    def is_confidence_enough(self,min_confidence_requiered=0.5):
        return  self.confidence > min_confidence_requiered 

    def get_color(self):
        return Entity.colors[self.category]

    def get_shape(self):
        return Entity.shapes[self.category]